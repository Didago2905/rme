from pathlib import Path

from core.models.media_item import MediaItem

from modules.analyzer.analyzer import Analyzer


class MediaService:

    def __init__(self):

        self._analyzer = Analyzer()

    def get_media(
        self,
        media_path: Path,
    ) -> MediaItem:

        return self._analyzer.analyze(
            media_path
        ).media_item