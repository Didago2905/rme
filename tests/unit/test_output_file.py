from pathlib import Path

from core.models.output_file import OutputFile


def test_output_file():
    output_file = OutputFile(
        source_path=Path(
            "data/samples/Samurai.Jack.2x01.HD720p-lat.mkv"
        ),
        output_path=Path(
            "data/output/Samurai.Jack.2x01.HD720p-lat.mp4"
        ),
        container="mp4",
        exists=False,
    )

    print(output_file)


if __name__ == "__main__":
    test_output_file()