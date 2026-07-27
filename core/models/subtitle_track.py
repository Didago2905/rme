from dataclasses import dataclass


@dataclass(slots=True)
class SubtitleTrack:
    codec: str

    language: str

    title: str