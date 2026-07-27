from dataclasses import dataclass

from core.models.parsed_episode import (
    ParsedEpisode,
)

from core.models.missing_episode import (
    MissingEpisode,
)


@dataclass(slots=True)
class SeasonMetadata:
    season_number: int

    episodes: list[ParsedEpisode]

    missing_episodes: list[MissingEpisode]