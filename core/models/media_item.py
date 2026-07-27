from dataclasses import dataclass

from pathlib import Path


@dataclass(slots=True)
class MediaItem:

    file_name: str

    path: Path