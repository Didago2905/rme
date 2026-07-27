from pathlib import Path

from core.models.library_metadata import (
    LibraryMetadata,
)

from modules.metadata.series_builder import (
    SeriesBuilder,
)

from modules.scanner.library_scanner import (
    LibraryScanner,
)


class LibraryBuilder:

    def __init__(self) -> None:

        self._scanner = LibraryScanner()

        self._series_builder = (
            SeriesBuilder()
        )

    def build(
        self,
        library_path: Path,
    ) -> LibraryMetadata:
        """
        Construye la metadata completa de una biblioteca.
        """

        series_metadata = []

        series_list = (
            self._scanner.scan_series(
                library_path
            )
        )

        for series in series_list:

            metadata = (
                self._series_builder.build(
                    series.path
                )
            )

            series_metadata.append(
                metadata
            )

        return LibraryMetadata(
            series=series_metadata
        )