from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from core.models.media_item import MediaItem


@dataclass(slots=True)
class ScanRoot:
    root_id: str
    path: Path


@dataclass(slots=True)
class ScanRootResult:
    root_id: str
    path: Path
    status: Literal["complete", "partial", "failed"]


@dataclass(slots=True)
class ScanItem:
    root_id: str
    relative_path: Path
    category: Literal["movie", "series"]
    media_item: MediaItem | None = None


@dataclass(slots=True)
class ScanAnomaly:
    root_id: str
    relative_path: Path | None
    code: str
    detail: str


@dataclass(slots=True)
class ScanResult:
    roots: list[ScanRootResult] = field(default_factory=list)
    items: list[ScanItem] = field(default_factory=list)
    anomalies: list[ScanAnomaly] = field(default_factory=list)
