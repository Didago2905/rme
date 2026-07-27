from dataclasses import dataclass

from core.models.season_metadata import (
    SeasonMetadata,
)


@dataclass(slots=True)
class SeriesMetadata:
    name: str

    seasons: list[SeasonMetadata]