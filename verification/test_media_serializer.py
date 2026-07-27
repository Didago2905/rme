from pathlib import Path

from modules.media.media_probe import (
    MediaProbe,
)

from modules.media.media_builder import (
    MediaBuilder,
)

from modules.media.media_serializer import (
    media_to_dict,
)


video_path = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

probe = MediaProbe()

raw_data = probe.probe(
    video_path
)

media = MediaBuilder().build(
    raw_data
)

print(
    media_to_dict(media)
)