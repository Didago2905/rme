from dataclasses import dataclass

from core.models.media_language import MediaLanguage


@dataclass(slots=True)
class AudioTrack:
    stream_index: int

    codec: str

    channels: int

    bitrate: int

    language: MediaLanguage

    title: str

    default: bool

    forced: bool