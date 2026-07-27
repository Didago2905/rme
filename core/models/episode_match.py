from dataclasses import dataclass


@dataclass(slots=True)
class EpisodeMatch:
    """
    Resultado del parseo
    de un nombre de episodio.
    """

    season_number: int

    episode_number: int