from pathlib import Path

from modules.metadata.season_parser import (
    SeasonParser,
)


parser = SeasonParser()

episodes = parser.parse(
    Path("data/samples")
)

print()

print(
    f"Parsed episodes: {len(episodes)}"
)

print()

for episode in episodes:
    print(episode)