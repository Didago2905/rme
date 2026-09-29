"""SQLite cache primitives; callers own the connection and transactions."""

import json
import math
import sqlite3
from collections.abc import Iterable
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import UnionType
from typing import get_args, get_origin

from core.models.media_item import MediaItem


def _relative_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/")
    normalized = PurePosixPath(text)
    if (
        normalized.is_absolute()
        or PureWindowsPath(text).drive
        or ".." in normalized.parts
        or not normalized.parts
    ):
        raise ValueError("Expected a nonempty relative media path without '..'.")
    return normalized.as_posix()


def _decode(value, expected):
    """Validate cached values against the current dataclass field types."""
    if get_origin(expected) is UnionType:
        for option in get_args(expected):
            try:
                return _decode(value, option)
            except (TypeError, ValueError):
                pass
        raise ValueError("Incompatible cached field type")
    if get_origin(expected) is list:
        if not isinstance(value, list):
            raise ValueError("Expected a cached list")
        return [_decode(item, get_args(expected)[0]) for item in value]
    if is_dataclass(expected):
        model_fields = fields(expected)
        if not isinstance(value, dict) or set(value) != {f.name for f in model_fields}:
            raise ValueError("Incompatible cached model fields")
        return expected(**{
            f.name: _decode(value[f.name], f.type) for f in model_fields
        })
    if expected is float:
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError("Expected a finite number")
    elif expected is Path:
        if not isinstance(value, Path):
            raise ValueError("Expected a media path")
    elif type(value) is not expected:
        raise ValueError("Incompatible cached field type")
    return value


class LibraryIndex:
    """Use an explicitly supplied connection on its owning thread.

    This class never commits, rolls back, or closes the connection. The caller
    controls transaction boundaries and must commit writes when appropriate.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        connection.execute("""
            CREATE TABLE IF NOT EXISTS library_files (
                root_id TEXT NOT NULL,
                relative_path TEXT NOT NULL,
                category TEXT NOT NULL CHECK (category IN ('movie', 'series')),
                size_bytes INTEGER NOT NULL,
                mtime_ns INTEGER NOT NULL,
                media_json TEXT,
                PRIMARY KEY (root_id, relative_path)
            )
        """)

    def lookup(self, root_id: str, relative_path: str | Path) -> dict | None:
        cursor = self._connection.execute(
            "SELECT root_id, relative_path, category, size_bytes, mtime_ns, "
            "media_json FROM library_files WHERE root_id = ? AND relative_path = ?",
            (root_id, _relative_path(relative_path)),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(zip((column[0] for column in cursor.description), row))

    def upsert(
        self,
        root_id: str,
        relative_path: str | Path,
        category: str,
        size_bytes: int,
        mtime_ns: int,
        media_item: MediaItem | None,
    ) -> None:
        media_json = None
        if media_item is not None:
            data = asdict(media_item)
            del data["path"]
            media_json = json.dumps(data, ensure_ascii=False, allow_nan=False)
        self._connection.execute(
            """
            INSERT INTO library_files
                (root_id, relative_path, category, size_bytes, mtime_ns, media_json)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(root_id, relative_path) DO UPDATE SET
                category = excluded.category,
                size_bytes = excluded.size_bytes,
                mtime_ns = excluded.mtime_ns,
                media_json = excluded.media_json
            """,
            (root_id, _relative_path(relative_path), category,
             size_bytes, mtime_ns, media_json),
        )

    def invalidate(self, root_id: str, relative_path: str | Path) -> None:
        """Clear technical analysis without deleting the discovered record."""
        self._connection.execute(
            "UPDATE library_files SET media_json = NULL "
            "WHERE root_id = ? AND relative_path = ?",
            (root_id, _relative_path(relative_path)),
        )

    def delete_missing(
        self, root_id: str, discovered_paths: Iterable[str | Path],
    ) -> int:
        """Delete unseen records only after successful, complete root discovery.

        Never call this for an unavailable or partially scanned root.
        An empty discovered set removes all records for this root only.
        """
        discovered = {_relative_path(path) for path in discovered_paths}
        rows = self._connection.execute(
            "SELECT relative_path FROM library_files WHERE root_id = ?", (root_id,),
        ).fetchall()
        missing = [(root_id, row[0]) for row in rows if row[0] not in discovered]
        self._connection.executemany(
            "DELETE FROM library_files WHERE root_id = ? AND relative_path = ?",
            missing,
        )
        return len(missing)

    @staticmethod
    def reconstruct_media(
        media_json: str | None,
        root_path: Path,
        relative_path: str | Path,
    ) -> MediaItem | None:
        """Return None for NULL, malformed, or incompatible cached analysis."""
        if media_json is None:
            return None
        try:
            data = json.loads(media_json)
            if not isinstance(data, dict) or "path" in data:
                return None
            data["path"] = root_path / _relative_path(relative_path)
            return _decode(data, MediaItem)
        except (ValueError, TypeError, KeyError, OverflowError, RecursionError):
            return None
