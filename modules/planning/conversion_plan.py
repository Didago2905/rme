from dataclasses import dataclass


@dataclass(slots=True)
class ConversionPlan:

    compatible: bool

    remux_container: bool

    convert_video: bool

    convert_audio: bool

    reason: str