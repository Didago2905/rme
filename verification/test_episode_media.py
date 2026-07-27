from pathlib import Path

from modules.metadata.library_builder import (
    LibraryBuilder,
)

from modules.media.media_probe import (
    MediaProbe,
)

from modules.media.media_builder import (
    MediaBuilder,
)


library = LibraryBuilder().build(
    Path(r"D:/Media/TestLibrary")
)

episode = (
    library
    .series[0]
    .seasons[0]
    .episodes[0]
)

print("\nEPISODE")
print("--------")
print(episode)

probe = MediaProbe()

raw_data = probe.probe(
    episode.media_item.path
)

media = MediaBuilder().build(
    raw_data
)

print("\nMEDIA")
print("-----")
print(media)