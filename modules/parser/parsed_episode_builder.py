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
        media_item: MediaItem,
    ) -> ParsedEpisode:

        match = self._parser.parse(
            media_item.file_name
        )

        if match is None:

            return ParsedEpisode(
                media_item=media_item,
                season_number=None,
                episode_number=None,
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