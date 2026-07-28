from dataclasses import dataclass


@dataclass(slots=True)
class ConversionJob:

    target_container: str

    convert_video: bool

    target_video_codec: str | None

    convert_audio: bool

    target_audio_codec: str | None