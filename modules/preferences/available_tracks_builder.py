from core.models.audio_track import AudioTrack
from core.models.available_tracks import AvailableTracks
from core.models.media_item import MediaItem
from core.models.subtitle_track import SubtitleTrack


class AvailableTracksBuilder:

    def build(
        self,
        media_items: list[MediaItem],
    ) -> AvailableTracks:

        audio_tracks = (
            self._collect_audio_tracks(
                media_items
            )
        )

        subtitle_tracks = (
            self._collect_subtitle_tracks(
                media_items
            )
        )

        return AvailableTracks(
            audio_tracks=audio_tracks,
            subtitle_tracks=subtitle_tracks,
        )

    def _collect_audio_tracks(
        self,
        media_items: list[MediaItem],
    ) -> list[AudioTrack]:

        tracks: list[AudioTrack] = []

        for media_item in media_items:

            for track in (
                media_item.audio_tracks
            ):

                if not any(
                    (
                        existing.language.code
                        == track.language.code
                        and existing.title
                        == track.title
                        and existing.codec
                        == track.codec
                        and existing.channels
                        == track.channels
                    )
                    for existing in tracks
                ):

                    tracks.append(track)

        return tracks

    def _collect_subtitle_tracks(
        self,
        media_items: list[MediaItem],
    ) -> list[SubtitleTrack]:

        tracks: list[SubtitleTrack] = []

        for media_item in media_items:

            for track in (
                media_item.subtitle_tracks
            ):

                if not any(
                    (
                        existing.language.code
                        == track.language.code
                        and existing.title
                        == track.title
                        and existing.codec
                        == track.codec
                        and existing.forced
                        == track.forced
                    )
                    for existing in tracks
                ):

                    tracks.append(track)

        return tracks