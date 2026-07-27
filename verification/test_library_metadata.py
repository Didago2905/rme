from core.models.library_metadata import (
    LibraryMetadata,
)

from core.models.series_metadata import (
    SeriesMetadata,
)


library = LibraryMetadata(
    series=[
        SeriesMetadata(
            name="Malcolm in the Middle",
            seasons=[],
        ),
        SeriesMetadata(
            name="Samurai Jack",
            seasons=[],
        ),
    ]
)

print(library)