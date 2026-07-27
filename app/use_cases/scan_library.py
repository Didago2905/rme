from pathlib import Path

from core.models.library_metadata import LibraryMetadata
from modules.metadata.library_builder import LibraryBuilder


class ScanLibraryUseCase:
    """
    Caso de uso encargado de iniciar el análisis de una biblioteca multimedia.
    """

    def __init__(self) -> None:
        self._library_builder = LibraryBuilder()

    def execute(
        self,
        library_path: str,
    ) -> LibraryMetadata:
        """
        Ejecuta el análisis de la biblioteca indicada.

        Args:
            library_path: Ruta de la biblioteca seleccionada por el usuario.
        """

        return self._library_builder.build(
            Path(library_path)
        )