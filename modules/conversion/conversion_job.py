from dataclasses import dataclass


@dataclass(slots=True)
class ConversionJob:

    # Container
    target_container: str

    # Video
    convert_video: bool
    target_video_codec: str | None

    # Audio
    convert_audio: bool
    target_audio_codec: str |None

    # Video options
    target_profile: str | None = None
    target_pixel_format: str | None = None
    target_level: float | None = None

    # Streams
    include_video: bool = True
    include_audio: bool = True
    include_subtitles: bool = False

    # Language preferences
    audio_languages: list[str] | None = None
    subtitle_languages: list[str] | None = None
    default_audio_language: str | None = None