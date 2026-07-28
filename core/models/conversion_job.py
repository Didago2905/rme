from dataclasses import dataclass


@dataclass(slots=True)
class ConversionJob:
    remux_container: bool = False

    convert_video: bool = False

    convert_audio: bool = False

    convert_subtitles: bool = False

    include_video: bool = True

    include_audio: bool = True

    include_subtitles: bool = False

    target_container: str = ""

    target_video_codec: str = ""

    target_audio_codec: str = ""

    target_subtitle_codec: str = ""
