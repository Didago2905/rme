from core.models.series_metadata import (
    SeriesMetadata,
)

from core.models.season_metadata import (
    SeasonMetadata,
)


series = SeriesMetadata(
    name="Malcolm in the Middle",
    seasons=[
        SeasonMetadata(
            season_number=1,
            episodes=[],
            missing_episodes=[],
        )
    ],
)

print(series)