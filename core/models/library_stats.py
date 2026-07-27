from dataclasses import dataclass


@dataclass(slots=True)
class LibraryStats:

    series_count: int

    episode_count: int

    missing_episode_count: int

    total_duration_hours: float

    languages: list[str]

    resolutions: list[str]