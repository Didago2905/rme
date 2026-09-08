from pathlib import Path

from modules.analyzer.analyzer import Analyzer


def test_analyzer():
    sample_dir = Path("data/samples")

    file_path = (
        sample_dir
        / "[locuranime.com]1080p X-Me97-2-01.mkv"
    )

    analyzer = Analyzer()

    result = analyzer.analyze(file_path)

    assert result.success is True

    media_item = result.media_item

    print("\n=== VIDEO TRACKS ===")

    for video in media_item.video_tracks:
        print(video)

    print("\n=== AUDIO TRACKS ===")

    for audio in media_item.audio_tracks:
        print(
            f"Stream: {audio.stream_index} | "
            f"Language: {audio.language.code} | "
            f"Title: {audio.title} | "
            f"Codec: {audio.codec} | "
            f"Default: {audio.default} | "
            f"Forced: {audio.forced}"
        )

    print("\n=== SUBTITLE TRACKS ===")

    for subtitle in media_item.subtitle_tracks:
        print(
            f"Stream: {subtitle.stream_index} | "
            f"Language: {subtitle.language.code} | "
            f"Title: {subtitle.title} | "
            f"Codec: {subtitle.codec} | "
            f"Default: {subtitle.default} | "
            f"Forced: {subtitle.forced}"
        )


if __name__ == "__main__":
    test_analyzer()