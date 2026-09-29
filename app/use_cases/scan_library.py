import sqlite3
from pathlib import Path

from core.constants.paths import LIBRARY_INDEX_PATH
from core.models.scan_result import (
    ScanAnomaly, ScanItem, ScanResult, ScanRoot, ScanRootResult,
)
from modules.library.library_index import LibraryIndex
from modules.media.media_service import MediaService
from modules.scanner.library_scanner import LibraryScanner


class ScanLibraryUseCase:
    """Observe media roots, reusing persisted technical analysis when unchanged."""

    def __init__(self) -> None:
        self._scanner = LibraryScanner()
        self._media_service = MediaService()

    def execute(self, roots: list[ScanRoot]) -> ScanResult:
        result = ScanResult()
        if not roots:
            return result
        if len({root.root_id for root in roots}) != len(roots):
            raise ValueError("Scan roots must have unique root_id values.")

        connection = None
        index = None

        def index_error(root_id: str, relative_path: Path | None, error: Exception) -> None:
            nonlocal index
            result.anomalies.append(ScanAnomaly(
                root_id, relative_path, "index_error", str(error),
            ))
            # Stop using an unreliable cache for the remainder of this scan.
            index = None

        def invalidate(root_id: str, relative_path: Path) -> None:
            if index is not None:
                try:
                    with connection:
                        index.invalidate(root_id, relative_path)
                except Exception as error:
                    index_error(root_id, relative_path, error)

        try:
            try:
                # The database parent is APP_STATE_DIR; creation is deferred
                # until execute opens the database on its current thread.
                LIBRARY_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
                connection = sqlite3.connect(LIBRARY_INDEX_PATH)
                with connection:
                    index = LibraryIndex(connection)
            except Exception as error:
                index_error(roots[0].root_id, None, error)

            for root in roots:
                root_result = ScanRootResult(root.root_id, root.path, "complete")
                result.roots.append(root_result)
                discovered_paths = set()

                def discovery_error(path: Path, error: OSError) -> None:
                    root_result.status = "partial"
                    result.anomalies.append(ScanAnomaly(
                        root.root_id, path.relative_to(root.path),
                        "discovery_failed", str(error),
                    ))

                try:
                    for category, path in self._scanner.discover_media_root(
                        root.path, discovery_error,
                    ):
                        item = ScanItem(root.root_id, path.relative_to(root.path), category)
                        result.items.append(item)
                        discovered_paths.add(item.relative_path)
                        fingerprint = None
                        try:
                            stat = path.stat()
                            fingerprint = (stat.st_size, stat.st_mtime_ns)
                        except OSError as error:
                            result.anomalies.append(ScanAnomaly(
                                root.root_id, item.relative_path, "stat_failed", str(error),
                            ))

                        if index is not None and fingerprint is not None:
                            try:
                                cached = index.lookup(root.root_id, item.relative_path)
                                if cached is not None and fingerprint == (
                                    cached["size_bytes"], cached["mtime_ns"],
                                ):
                                    media = index.reconstruct_media(
                                        cached["media_json"], root.path, item.relative_path,
                                    )
                                    if media is not None and (
                                        media.video_tracks or media.audio_tracks or media.subtitle_tracks
                                    ):
                                        item.media_item = media
                                        continue
                            except Exception as error:
                                index_error(root.root_id, item.relative_path, error)

                        # Clear obsolete analysis before probing, including when
                        # stat failed, so a failed probe cannot leave a reusable row.
                        invalidate(root.root_id, item.relative_path)
                        try:
                            item.media_item = self._media_service.get_media(path)
                        except Exception as error:
                            result.anomalies.append(ScanAnomaly(
                                root.root_id, item.relative_path,
                                "analysis_failed", str(error),
                            ))
                            continue

                        media = item.media_item
                        if not (media.video_tracks or media.audio_tracks or media.subtitle_tracks):
                            result.anomalies.append(ScanAnomaly(
                                root.root_id, item.relative_path,
                                "analysis_empty", "Analysis returned no media tracks.",
                            ))

                        try:
                            stat = path.stat()
                            after = (stat.st_size, stat.st_mtime_ns)
                        except OSError as error:
                            result.anomalies.append(ScanAnomaly(
                                root.root_id, item.relative_path, "stat_failed", str(error),
                            ))
                            continue
                        if fingerprint is None:
                            continue
                        if after != fingerprint:
                            result.anomalies.append(ScanAnomaly(
                                root.root_id, item.relative_path, "file_changed",
                                "File changed during analysis; result was not cached.",
                            ))
                            continue

                        if index is not None:
                            try:
                                with connection:
                                    index.upsert(
                                        root.root_id, item.relative_path, category,
                                        fingerprint[0], fingerprint[1], media,
                                    )
                            except Exception as error:
                                index_error(root.root_id, item.relative_path, error)
                except OSError as error:
                    root_result.status = "failed"
                    result.anomalies.append(ScanAnomaly(
                        root.root_id, None, "root_unavailable", str(error),
                    ))

                if index is not None and root_result.status == "complete":
                    try:
                        with connection:
                            index.delete_missing(root.root_id, discovered_paths)
                    except Exception as error:
                        index_error(root.root_id, None, error)
        finally:
            if connection is not None:
                try:
                    connection.close()
                except sqlite3.Error as error:
                    index_error(roots[0].root_id, None, error)
        return result
