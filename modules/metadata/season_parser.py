from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)

from modules.analyzer.analyzer import (
    Analyzer,
)

from modules.parser.parsed_episode_builder import (
    ParsedEpisodeBuilder,
)

from modules.scanner.library_scanner import (
    LibraryScanner,
)


class SeasonParser:

    def __init__(self):

        self._scanner = LibraryScanner()

        self._builder = ParsedEpisodeBuilder()

        self._analyzer = Analyzer()

    def parse(
        self,
        season_path: Path,
    ) -> list[ParsedEpisode]:

        parsed_episodes = []

        episode_infos = self._scanner.scan_episodes(
            season_path
        )

        for episode_info in episode_infos:

            analysis_result = self._analyzer.analyze(
                episode_info.path
            )

            parsed_episode = (
                self._builder.build(
                    analysis_result.media_item
                )
            )

            if parsed_episode:

                parsed_episodes.append(
                    parsed_episode
                )

        return parsed_episodes