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

    @property
    def duration_formatted(self) -> str:
        total_seconds = int(self.duration_seconds)

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"

        return f"{minutes:02}:{seconds:02}"

    @property
    def total_frames(self) -> int:

        if not self.video_tracks:
            return 0

        try:
            frame_rate = float(self.video_tracks[0].frame_rate)
        except (TypeError, ValueError):
            return 0

        return int(round(self.duration_seconds * frame_rate))