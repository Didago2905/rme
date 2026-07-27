from dataclasses import dataclass

from core.models.media_item import (
    MediaItem,
)


@dataclass(slots=True)
class ParsedEpisode:
    """
    Episodio con información
    estructurada extraída del nombre.
    """

    media_item: MediaItem

    season_number: int

    episode_number: int