from modules.parser.episode_parser import (
    EpisodeParser,
)


parser = EpisodeParser()

samples = [
    "Samurai.Jack.2x01.HD720p-lat.mkv",
    "Futurama.S03E12.1080p.mkv",
    "Batman.S01E05.mp4",
    "archivo_sin_patron.mkv",
]

for sample in samples:

    result = parser.parse(
        sample
    )

    print()
    print(sample)
    print(result)