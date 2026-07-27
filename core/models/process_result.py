from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProcessResult:
    """
    Resultado del procesamiento
    de un archivo individual.
    """

    success: bool

    skipped: bool = False

    input_path: Path | None = None

    output_path: Path | None = None

    error: str | None = None