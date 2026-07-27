from pathlib import Path

from core.models.series_metadata import (
    SeriesMetadata,
)

from modules.metadata.season_builder import (
    SeasonBuilder,
)

from modules.scanner.library_scanner import (
    LibraryScanner,
)


class SeriesBuilder:

    def __init__(self) -> None:

        self._scanner = LibraryScanner()

        self._season_builder = (
            SeasonBuilder()
        )

    def build(
        self,
        series_path: Path,
    ) -> SeriesMetadata:
        """
        Construye el modelo de una serie a partir de su carpeta.
        """

        season_metadata = []

        seasons = (
            self._scanner.scan_seasons(
                series_path
            )
        )

        for season in seasons:

            metadata = (
                self._season_builder.build(
                    season.path
                )
            )

            season_metadata.append(
                metadata
            )

        return SeriesMetadata(
            name=series_path.name,
            seasons=season_metadata,
        )