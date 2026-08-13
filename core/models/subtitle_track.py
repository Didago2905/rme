from dataclasses import dataclass

from core.models.media_language import (
    MediaLanguage,
)


@dataclass(slots=True)
class SubtitleTrack:
    stream_index: int

    codec: str

    language: MediaLanguage

    title: str

    default: bool

    forced: bool