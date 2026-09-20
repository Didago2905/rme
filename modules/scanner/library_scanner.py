from pathlib import Path

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