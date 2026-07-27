from pathlib import Path

from core.models.season_info import SeasonInfo


season = SeasonInfo(
    name="Season 01",
    path=Path(
        "D:/Media/Series/Samurai Jack/Season 01"
    ),
)

print(season)