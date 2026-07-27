from pathlib import Path

from core.models.media_file import MediaFile
from modules.media.media_service import MediaService


class AnalyzeMediaUseCase:
    """
    Caso de uso encargado de analizar un archivo multimedia.
    """

    def __init__(self) -> None:
        self._media_service = MediaService()

    def execute(
        self,
        media_path: Path,
    ) -> MediaFile:
        """
        Analiza un archivo multimedia y devuelve su
        información técnica.
        """

        return self._media_service.get_media(
            media_path
        )