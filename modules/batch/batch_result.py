from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BatchResult:
    """
    Resultado del procesamiento de un archivo individual.
    """

    file_path: Path

    success: bool

    skipped: bool = False

    output_path: Path | None = None

    error: str | None = None