from pathlib import Path
from collections.abc import Callable, Iterator
from typing import Literal

from core.models.series_info import SeriesInfo
from core.models.season_info import SeasonInfo
from core.models.episode_info import EpisodeInfo


SUPPORTED_EXTENSIONS = {
    ".mkv",
    ".mp4",
    ".m4v",
    ".avi",
    ".mov",
    ".wmv",
}


class LibraryScanner:

    def discover_media_root(
        self,
        root_path: Path,
        on_error: Callable[[Path, OSError], None],
    ) -> Iterator[tuple[Literal["movie", "series"], Path]]:
        """Discover Movies/ and Series/, reporting incomplete traversal.

        Missing categories are allowed; root access errors propagate.
        Directory symlinks are not followed to avoid traversal cycles.
        """
        entries = {entry.name: entry for entry in root_path.iterdir()}

        def walk(directory: Path) -> Iterator[Path]:
            try:
                children = sorted(directory.iterdir())
            except OSError as error:
                on_error(directory, error)
                return
            for child in children:
                try:
                    if child.is_dir():
                        if not child.is_symlink():
                            yield from walk(child)
                    elif child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                        yield child
                except OSError as error:
                    on_error(child, error)

        categories: tuple[tuple[str, Literal["movie", "series"]], ...] = (
            ("Movies", "movie"), ("Series", "series"),
        )
        for name, category in categories:
            directory = entries.get(name)
            if directory is None:
                continue
            try:
                if not directory.is_dir() or directory.is_symlink():
                    raise OSError(f"Expected a regular category directory: {directory}")
            except OSError as error:
                on_error(directory, error)
                continue
            for path in walk(directory):
                yield category, path

    def scan(
        self,
        library_path: Path,
    ) -> list[Path]:

        files = []

        for file in library_path.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower()
                in SUPPORTED_EXTENSIONS
            ):
                files.append(file)

        return sorted(files)

    def scan_series(
        self,
        library_path: Path,
    ) -> list[SeriesInfo]:

        series = []

        for item in sorted(
            library_path.iterdir()
        ):

            if item.is_dir():

                series.append(
                    SeriesInfo(
                        name=item.name,
                        path=item,
                    )
                )

        return series

    def scan_seasons(
        self,
        series_path: Path,
    ) -> list[SeasonInfo]:

        seasons = []

        for item in sorted(
            series_path.iterdir()
        ):

            if item.is_dir():

                seasons.append(
                    SeasonInfo(
                        name=item.name,
                        path=item,
                    )
                )

        return seasons

    def scan_episodes(
        self,
        season_path: Path,
    ) -> list[EpisodeInfo]:

        episodes = []

        for item in sorted(
            season_path.iterdir()
        ):

            if (
                item.is_file()
                and item.suffix.lower()
                in SUPPORTED_EXTENSIONS
            ):

                episodes.append(
                    EpisodeInfo(
                        file_name=item.name,
                        path=item,
                    )
                )

        return episodes
