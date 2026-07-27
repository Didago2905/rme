from dataclasses import dataclass, field


@dataclass(slots=True)
class CompatibilityReport:
    is_compatible: bool = False

    profile_name: str = ""

    score: int = 0

    issues: list[str] = field(default_factory=list)

    container_compatible: bool = False

    video_compatible: bool = False

    audio_compatible: bool = False

    subtitle_compatible: bool = False