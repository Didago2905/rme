from pathlib import Path

from modules.media.media_service import (
    MediaService,
)


video_path = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

service = MediaService()

media = service.get_media(
    video_path
)

print(media)