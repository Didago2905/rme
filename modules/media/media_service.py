from pathlib import Path

from core.models.media_file import (
    MediaFile,
)

from modules.media.media_probe import (
    MediaProbe,
)

from modules.media.media_builder import (
    MediaBuilder,
)


class MediaService:

    def __init__(self):

        self._probe = (
            MediaProbe()
        )

        self._builder = (
            MediaBuilder()
        )

    def get_media(
        self,
        media_path: Path,
    ) -> MediaFile:

        raw_media = self._probe.probe(
            media_path
        )

        media = self._builder.build(
            raw_media
        )

        return media