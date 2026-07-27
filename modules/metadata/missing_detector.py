from core.models.missing_episode import (
    MissingEpisode,
)

from core.models.parsed_episode import (
    ParsedEpisode,
)


class MissingDetector:

    def detect(
        self,
        episodes: list[ParsedEpisode],
    ) -> list[MissingEpisode]:

        if not episodes:
            return []

        episode_numbers = sorted(
            episode.episode_number
            for episode in episodes
        )

        first_episode = episode_numbers[0]

        last_episode = episode_numbers[-1]

        existing = set(
            episode_numbers
        )

        missing = []

        for number in range(
            first_episode,
            last_episode + 1,
        ):

            if number not in existing:

                missing.append(
                    MissingEpisode(
                        episode_number=number,
                    )
                )

        return missing