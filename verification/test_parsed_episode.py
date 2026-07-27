from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)


episode = ParsedEpisode(
    file_name="Samurai.Jack.2x01.HD720p-lat.mkv",
    path=Path(
        "D:/Media/Series/Samurai Jack/Season 02"
    ),
    season_number=2,
    episode_number=1,
)

print(episode)