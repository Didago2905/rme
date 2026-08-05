from dataclasses import dataclass


@dataclass(slots=True)
class VideoTrack:
    codec: str

    width: int

    height: int

    bitrate: int

    fps: float

    profile: str

    level: float | None

    pixel_format: str

    color_space: str

    field_order: str