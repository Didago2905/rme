from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class EpisodeInfo:

    file_name: str

    path: Path