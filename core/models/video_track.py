from dataclasses import dataclass


@dataclass(slots=True)
class VideoTrack:
    codec: str

    width: int

    height: int

    frame_rate: str

    pixel_format: str

    profile: str

    level: str

    scan_type: str