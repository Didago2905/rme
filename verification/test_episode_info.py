from pathlib import Path

from core.models.episode_info import EpisodeInfo


episode = EpisodeInfo(
    file_name="Samurai.Jack.S01E01.mkv",
    path=Path(
        "D:/Media/Series/Samurai Jack/Season 01"
    ),
)

print(episode)