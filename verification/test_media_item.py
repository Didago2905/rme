from pathlib import Path

from core.models.media_item import (
    MediaItem,
)


item = MediaItem(
    file_name="movie.mkv",
    path=Path(
        "D:/Media/movie.mkv"
    ),
)

print(item)