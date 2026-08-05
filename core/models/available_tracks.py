from dataclasses import dataclass

from core.models.media_language import (
    MediaLanguage,
)


@dataclass(slots=True)
class AvailableTracks:

    audio_languages: list[MediaLanguage]

    subtitle_languages: list[MediaLanguage]