from core.models.episode_info import (
    EpisodeInfo,
)

from core.models.media_item import (
    MediaItem,
)

from core.models.parsed_episode import (
    ParsedEpisode,
)

from modules.parser.episode_parser import (
    EpisodeParser,
)


class ParsedEpisodeBuilder:

    def __init__(self):

        self._parser = (
            EpisodeParser()
        )

    def build(
        self,
        episode: EpisodeInfo,
    ) -> ParsedEpisode | None:

        match = self._parser.parse(
            episode.file_name
        )

        if match is None:

            return None

        media_item = (
            MediaItem(
                file_name=episode.file_name,
                path=episode.path,
            )
        )

        return ParsedEpisode(
            media_item=media_item,
            season_number=(
                match.season_number
            ),
            episode_number=(
                match.episode_number
            ),
        )