from dataclasses import dataclass

from core.models.video_track import (
    VideoTrack,
)

from core.models.audio_track import (
    AudioTrack,
)

from core.models.subtitle_track import (
    SubtitleTrack,
)


@dataclass(slots=True)
class MediaFile:
    container: str

    duration_seconds: float

    size_bytes: int

    bitrate: int

    video_tracks: list[VideoTrack]

    audio_tracks: list[AudioTrack]

    subtitle_tracks: list[SubtitleTrack]