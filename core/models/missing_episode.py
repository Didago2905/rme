from dataclasses import dataclass


@dataclass(slots=True)
class MissingEpisode:
    episode_number: int