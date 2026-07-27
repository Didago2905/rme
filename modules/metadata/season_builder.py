from pathlib import Path

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

        missing = (
            self._missing_detector.detect(
                episodes
            )
        )

        season_number = 0

        if episodes:

            season_number = (
                episodes[0].season_number
            )

        return SeasonMetadata(
            season_number=season_number,
            episodes=episodes,
            missing_episodes=missing,
        )