from pathlib import Path

from core.models.episode_info import (
    EpisodeInfo,
)

from modules.parser.parsed_episode_builder import (
    ParsedEpisodeBuilder,
)


builder = ParsedEpisodeBuilder()

episode = EpisodeInfo(
    file_name="Samurai.Jack.2x01.HD720p-lat.mkv",
    path=Path(
        "data/samples/Samurai.Jack.2x01.HD720p-lat.mkv"
    ),
)

result = builder.build(
    episode
)

print(result)