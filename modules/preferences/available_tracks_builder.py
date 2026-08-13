from core.models.available_tracks import (
    AvailableTracks,
)

from core.models.parsed_episode import (
    ParsedEpisode,
)


class AvailableTracksBuilder:

    def build(
        self,
        episodes: list[ParsedEpisode],
    ) -> AvailableTracks:

        audio_tracks = (
            self._collect_audio_tracks(
                episodes
            )
        )

        subtitle_tracks = (
            self._collect_subtitle_tracks(
                episodes
            )
        )

        return AvailableTracks(
            audio_tracks=audio_tracks,
            subtitle_tracks=subtitle_tracks,
        )

    def _collect_audio_tracks(
        self,
        episodes: list[ParsedEpisode],
    ) -> list:

        tracks = []

        for episode in episodes:

            for track in (
                episode.media_item.audio_tracks
            ):

                if not any(
                    existing.stream_index
                    == track.stream_index
                    and existing.language.code
                    == track.language.code
                    for existing in tracks
                ):
                    tracks.append(track)

        return tracks

    def _collect_subtitle_tracks(
        self,
        episodes: list[ParsedEpisode],
    ) -> list:

        tracks = []

        for episode in episodes:

            for track in (
                episode.media_item.subtitle_tracks
            ):

                if not any(
                    existing.stream_index
                    == track.stream_index
                    and existing.language.code
                    == track.language.code
                    for existing in tracks
                ):
                    tracks.append(track)

        return tracks