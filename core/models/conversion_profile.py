from dataclasses import dataclass, field


@dataclass(slots=True)
class ConversionProfile:
    name: str = ""

    video_codec: str = ""

    audio_codec: str = ""

    subtitle_codec: str = ""

    allowed_containers: list[str] = field(default_factory=list)