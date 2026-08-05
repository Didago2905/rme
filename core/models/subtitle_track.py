from dataclasses import dataclass

from core.models.media_language import (
    MediaLanguage,
)


@dataclass(slots=True)
class SubtitleTrack:
    codec: str

    language: MediaLanguage