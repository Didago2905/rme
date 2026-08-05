from core.models.available_tracks import (
    AvailableTracks,
)

from core.models.media_language import (
    MediaLanguage,
)

from core.models.parsed_episode import (
    ParsedEpisode,
)


class AvailableTracksBuilder:

    def build(
        self,
        episodes: list[ParsedEpisode],
    ) -> AvailableTracks:

        audio_languages = (
            self._collect_audio_languages(
                episodes
            )
        )

        subtitle_languages = (
            self._collect_subtitle_languages(
                episodes
            )
        )

        return AvailableTracks(
            audio_languages=audio_languages,
            subtitle_languages=subtitle_languages,
        )

    def _collect_audio_languages(
        self,
        episodes: list[ParsedEpisode],
    ) -> list[MediaLanguage]:

        languages: dict[str, MediaLanguage] = {}

        for episode in episodes:

            for track in (
                episode.media_item.audio_tracks
            ):

                if (
                    track.language.code
                    not in languages
                ):

                    languages[
                        track.language.code
                    ] = track.language

        return list(
            languages.values()
        )

    def _collect_subtitle_languages(
        self,
        episodes: list[ParsedEpisode],
    ) -> list[MediaLanguage]:

        languages: dict[str, MediaLanguage] = {}

        for episode in episodes:

            for track in (
                episode.media_item.subtitle_tracks
            ):

                if (
                    track.language.code
                    not in languages
                ):

                    languages[
                        track.language.code
                    ] = track.language

        return list(
            languages.values()
        )