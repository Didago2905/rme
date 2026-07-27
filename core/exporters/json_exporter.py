import json

from pathlib import Path

from core.models.library_metadata import (
    LibraryMetadata,
)

from modules.media.media_service import (
    MediaService,
)

from modules.media.media_serializer import (
    media_to_dict,
)


class JsonExporter:

    @staticmethod
    def export_library(
        library: LibraryMetadata,
        output_path: Path,
    ) -> None:

        media_service = (
            MediaService()
        )

        data = {
            "series": []
        }

        for series in library.series:

            series_data = {
                "name": series.name,
                "seasons": [],
            }

            for season in series.seasons:

                season_data = {
                    "season_number": season.season_number,
                    "episodes": [],
                    "missing_episodes": [],
                }

                for episode in season.episodes:

                    media = (
                        media_service.get_media(
                            episode.media_item.path
                        )
                    )

                    episode_data = {
                        "season_number": episode.season_number,
                        "episode_number": episode.episode_number,
                        "file": {
                            "name": episode.media_item.file_name,
                            "path": str(
                                episode.media_item.path
                            ),
                        },
                        "media": media_to_dict(
                            media
                        ),
                        "metadata": None,
                    }

                    season_data[
                        "episodes"
                    ].append(
                        episode_data
                    )

                season_data[
                    "missing_episodes"
                ] = [
                    missing.episode_number
                    for missing in season.missing_episodes
                ]

                series_data[
                    "seasons"
                ].append(
                    season_data
                )

            data[
                "series"
            ].append(
                series_data
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )