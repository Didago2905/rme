from dataclasses import dataclass


@dataclass(slots=True)
class FFmpegProgress:
    frame: int
    time_seconds: float