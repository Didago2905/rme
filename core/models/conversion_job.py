from dataclasses import dataclass

from core.models.audio_track import AudioTrack
from core.models.subtitle_track import SubtitleTrack


@dataclass(slots=True)
class ConversionJob:
    # Actions
    remux_container: bool = False

    convert_video: bool = False
    convert_audio: bool = False
    convert_subtitles: bool = False

    # Streams
    include_video: bool = True
    include_audio: bool = True
    include_subtitles: bool = False

    # Container
    target_container: str = ""

    # Video
    target_video_codec: str = ""
    target_profile: str | None = None
    target_pixel_format: str | None = None
    target_level: float | None = None

    # Audio
    target_audio_codec: str = ""

    # Subtitles
    target_subtitle_codec: str = ""

    # Selected tracks
    audio_tracks: list[AudioTrack] | None = None

    subtitle_tracks: list[SubtitleTrack] | None = None

    default_audio_track: AudioTrack | None = None