from pathlib import Path

from modules.media.media_probe import (
    MediaProbe,
)


video_path = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

probe = MediaProbe()

data = probe.probe(video_path)

print(data.keys())