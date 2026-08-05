from dataclasses import dataclass

from core.models.media_language import MediaLanguage


@dataclass(slots=True)
class AudioTrack:
    codec: str

    channels: int

    bitrate: int

    language: MediaLanguage

    default: bool

    forced: bool