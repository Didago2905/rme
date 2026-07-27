from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SeasonInfo:
    """
    Información básica de una temporada
    descubierta en la biblioteca.
    """

    name: str

    path: Path