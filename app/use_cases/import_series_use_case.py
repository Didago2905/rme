from pathlib import Path

from core.models.series_metadata import (
    SeriesMetadata,
)

from modules.metadata.series_builder import (
    SeriesBuilder,
)


class ImportSeriesUseCase:

    def __init__(self) -> None:

        self._series_builder = (
            SeriesBuilder()
        )

    def execute(
        self,
        series_path: str,
    ) -> SeriesMetadata:
        """
        Construye los metadatos de una serie.
        """

        return self._series_builder.build(
            Path(series_path)
        )