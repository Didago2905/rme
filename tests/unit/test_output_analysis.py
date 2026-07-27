from pathlib import Path

from modules.analyzer.analyzer import Analyzer


def test_output_analysis():
    output_dir = Path("data/output")

    file_path = next(output_dir.glob("*.mp4"))

    analyzer = Analyzer()

    result = analyzer.analyze(file_path)

    print()
    print("FILE")
    print(result.media_file.file_name)

    print()

    print("CONTAINER")
    print(result.media_file.container)

    print()

    print("VIDEO TRACKS")
    for video in result.media_file.video_tracks:
        print(video)

    print()

    print("AUDIO TRACKS")
    for audio in result.media_file.audio_tracks:
        print(audio)

    print()

    print("SUBTITLE TRACKS")
    for subtitle in result.media_file.subtitle_tracks:
        print(subtitle)


if __name__ == "__main__":
    test_output_analysis()