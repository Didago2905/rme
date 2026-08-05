from dataclasses import dataclass

from core.models.media_item import MediaItem


@dataclass(slots=True)
class AnalysisResult:
    media_item: MediaItem

    success: bool = False

    analyzer: str = ""

    error_message: str = ""