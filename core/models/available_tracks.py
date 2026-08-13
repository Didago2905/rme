from dataclasses import dataclass

from core.models.audio_track import (
    AudioTrack,
)
from core.models.subtitle_track import (
    SubtitleTrack,
)


@dataclass(slots=True)
class AvailableTracks:

    audio_tracks: list[AudioTrack]

    subtitle_tracks: list[SubtitleTrack]