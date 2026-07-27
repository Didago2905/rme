from dataclasses import dataclass

from core.models.series_metadata import (
    SeriesMetadata,
)


@dataclass(slots=True)
class LibraryMetadata:
    series: list[SeriesMetadata]