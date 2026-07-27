import re

from core.models.episode_match import EpisodeMatch


class EpisodeParser:

    PATTERNS = [
        re.compile(
            r"(?i)s(\d+)e(\d+)"
        ),
        re.compile(
            r"(?i)(\d+)x(\d+)"
        ),
    ]

    def parse(
        self,
        file_name: str,
    ) -> EpisodeMatch | None:

        for pattern in self.PATTERNS:

            match = pattern.search(
                file_name
            )

            if match:

                return EpisodeMatch(
                    season_number=int(
                        match.group(1)
                    ),
                    episode_number=int(
                        match.group(2)
                    ),
                )

        return None