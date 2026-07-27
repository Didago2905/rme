from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)

from modules.scanner.library_scanner import (
    LibraryScanner,
)

from modules.parser.parsed_episode_builder import (
    ParsedEpisodeBuilder,
)


class SeasonParser:

    def __init__(self):

        self._scanner = LibraryScanner()

        self._builder = ParsedEpisodeBuilder()

    def parse(
        self,
        season_path: Path,
    ) -> list[ParsedEpisode]:

        parsed_episodes = []

        episodes = self._scanner.scan_episodes(
            season_path
        )

        for episode in episodes:

            parsed_episode = (
                self._builder.build(
                    episode
                )
            )

            if parsed_episode:

                parsed_episodes.append(
                    parsed_episode
                )

        return parsed_episodes