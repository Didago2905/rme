from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)

from modules.metadata.missing_detector import (
    MissingDetector,
)


episodes = [
    ParsedEpisode(
        file_name="S01E01.mkv",
        path=Path("S01E01.mkv"),
        season_number=1,
        episode_number=1,
    ),
    ParsedEpisode(
        file_name="S01E02.mkv",
        path=Path("S01E02.mkv"),
        season_number=1,
        episode_number=2,
    ),
    ParsedEpisode(
        file_name="S01E04.mkv",
        path=Path("S01E04.mkv"),
        season_number=1,
        episode_number=4,
    ),
]

detector = MissingDetector()

missing = detector.detect(
    episodes
)

print()

print(
    f"Missing episodes: {len(missing)}"
)

print()

for episode in missing:
    print(episode)