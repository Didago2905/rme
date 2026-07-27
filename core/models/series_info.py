from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SeriesInfo:
    """
    Información básica de una serie
    descubierta en la biblioteca.
    """

    name: str

    path: Path