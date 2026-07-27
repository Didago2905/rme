from dataclasses import dataclass


@dataclass(slots=True)
class AudioTrack:
    codec: str

    channels: int

    language: str

    title: str