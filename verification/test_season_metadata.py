from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)

from core.models.missing_episode import (
    MissingEpisode,
)

from core.models.season_metadata import (
    SeasonMetadata,
)


metadata = SeasonMetadata(
    season_number=1,
    episodes=[
        ParsedEpisode(
            file_name="S01E01.mkv",
            path=Path("S01E01.mkv"),
            season_number=1,
            episode_number=1,
        )
    ],
    missing_episodes=[
        MissingEpisode(
            episode_number=2
        )
    ],
)

print(metadata)