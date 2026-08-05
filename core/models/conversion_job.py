from dataclasses import dataclass


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

    audio_languages: list[str] | None = None

    subtitle_languages: list[str] | None = None

    default_audio_language: str | None = None