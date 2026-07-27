from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class OutputFile:
    source_path: Path

    output_path: Path

    container: str = ""

    exists: bool = False