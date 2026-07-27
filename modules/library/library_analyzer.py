from core.models.library_metadata import (
    LibraryMetadata,
)

from core.models.library_stats import (
    LibraryStats,
)

from modules.media.media_service import (
    MediaService,
)


class LibraryAnalyzer:

    def __init__(self):

        self._media_service = (
            MediaService()
        )

    def analyze(
        self,
        library: LibraryMetadata,
    ) -> LibraryStats:

        series_count = 0

        episode_count = 0

        missing_episode_count = 0

        total_seconds = 0.0

        languages = set()

        resolutions = set()

        for series in library.series:

            series_count += 1

            for season in series.seasons:

                missing_episode_count += len(
                    season.missing_episodes
                )

                for episode in season.episodes:

                    episode_count += 1

                    media = (
                        self._media_service.get_media(
                            episode.media_item.path
                        )
                    )

                    total_seconds += (
                        media.duration_seconds
                    )

                    for audio in (
                        media.audio_tracks
                    ):

                        if audio.language:

                            languages.add(
                                audio.language
                            )

                    for video in (
                        media.video_tracks
                    ):

                        if video.height:

                            resolutions.add(
                                f"{video.height}p"
                            )

        return LibraryStats(

            series_count=series_count,

            episode_count=episode_count,

            missing_episode_count=(
                missing_episode_count
            ),

            total_duration_hours=round(
                total_seconds / 3600,
                2,
            ),

            languages=sorted(
                languages
            ),

            resolutions=sorted(
                resolutions
            ),
        )