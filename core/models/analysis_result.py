from dataclasses import dataclass

from core.models.media_file import MediaFile


@dataclass(slots=True)
class AnalysisResult:
    media_file: MediaFile

    success: bool = False

    analyzer: str = ""

    error_message: str = ""