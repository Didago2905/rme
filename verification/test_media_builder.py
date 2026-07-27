from pathlib import Path

from modules.media.media_probe import (
    MediaProbe,
)

from modules.media.media_builder import (
    MediaBuilder,
)


video_path = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

probe = MediaProbe()

data = probe.probe(
    video_path
)

media = MediaBuilder().build(
    data
)

print(media)