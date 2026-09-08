import re
from pathlib import Path

from core.models.parsed_episode import (
    ParsedEpisode,
)

from core.models.season_metadata import (
    SeasonMetadata,
)

from modules.metadata.missing_detector import (
    MissingDetector,
)

from modules.metadata.season_parser import (
    SeasonParser,
)


class SeasonBuilder:

    def __init__(self) -> None:

        self._season_parser = (
            SeasonParser()
        )

        self._missing_detector = (
            MissingDetector()
        )

    def build(
        self,
        season_path: Path,
    ) -> SeasonMetadata:

        episodes = (
            self._season_parser.parse(
                season_path
            )
        )

        season_number = (
            self._parse_season_number(
                season_path.name
            )
        )

        if season_number is None:

            season_number = (
                self._detect_episode_season(
                    episodes
                )
            )

        episodes = (
            self._complete_episode_numbers(
                episodes,
                season_number,
            )
        )

        missing = (
            self._missing_detector.detect(
                episodes
            )
        )

        return SeasonMetadata(
            season_number=season_number,
            episodes=episodes,
            missing_episodes=missing,
        )

    def _parse_season_number(
        self,
        folder_name: str,
    ) -> int | None:

        match = re.fullmatch(
            r"(?i)(?:season|temporada)\s*0*(\d+)",
            folder_name.strip(),
        )

        if match is None:
            return None

        return int(
            match.group(1)
        )

    def _detect_episode_season(
        self,
        episodes: list[ParsedEpisode],
    ) -> int | None:

        for episode in episodes:

            if episode.season_number is not None:

                return episode.season_number

        return None

    def _complete_episode_numbers(
        self,
        episodes: list[ParsedEpisode],
        season_number: int | None,
    ) -> list[ParsedEpisode]:

        if not episodes:
            return []

        existing_numbers = {
            episode.episode_number
            for episode in episodes
            if episode.episode_number is not None
        }

        next_number = 1

        completed = []

        for episode in episodes:

            episode_number = (
                episode.episode_number
            )

            if episode_number is None:

                while next_number in existing_numbers:
                    next_number += 1

                episode_number = next_number

                existing_numbers.add(
                    episode_number
                )

                next_number += 1

            completed.append(
                ParsedEpisode(
                    media_item=episode.media_item,
                    season_number=season_number,
                    episode_number=episode_number,
                )
            )

        return completed