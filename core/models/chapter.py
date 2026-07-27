from dataclasses import dataclass


@dataclass(slots=True)
class Chapter:
    title: str = ""

    start_seconds: float = 0.0

    end_seconds: float = 0.0