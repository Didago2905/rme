from dataclasses import dataclass
from pathlib import Path

from core.models.audio_track import AudioTrack
from core.models.subtitle_track import SubtitleTrack
from core.models.video_track import VideoTrack


@dataclass(slots=True)
class MediaItem:
    file_name: str

    path: Path

    container: str

    duration_seconds: float

    size_bytes: int

    bitrate: int

    video_tracks: list[VideoTrack]

    audio_tracks: list[AudioTrack]

    subtitle_tracks: list[SubtitleTrack]

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

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
            fps = self.video_tracks[0].fps
        except (TypeError, ValueError):
            return 0

        return int(round(self.duration_seconds * fps))