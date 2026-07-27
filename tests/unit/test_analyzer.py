from pathlib import Path

from modules.analyzer.analyzer import Analyzer


def test_analyzer():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    analyzer = Analyzer()

    result = analyzer.analyze(file_path)

    for video in result.media_file.video_tracks:
        print(video)


if __name__ == "__main__":
    test_analyzer()