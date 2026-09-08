from modules.converter.ffmpeg_progress_parser import (
    FFmpegProgressParser,
)


def test_ffmpeg_progress_parser() -> None:
    parser = FFmpegProgressParser()

    progress = None

    test_lines = [
        "frame=8",
        "fps=7.79",
        "out_time_ms=N/A",
        "out_time=N/A",
        "progress=continue",
    ]

    for line in test_lines:
        result = parser.parse(line)

        if result is not None:
            progress = result

    assert progress is not None
    assert progress.frame == 8
    assert progress.time_seconds is None

    print("\n=== PROGRESS RESULT ===")
    print(f"Frame: {progress.frame}")
    print(f"Time: {progress.time_seconds}")


if __name__ == "__main__":
    test_ffmpeg_progress_parser()

def test_ffmpeg_progress_with_time() -> None:
    parser = FFmpegProgressParser()

    progress = None

    test_lines = [
        "frame=100",
        "fps=24.00",
        "out_time_ms=5000000",
        "out_time=00:00:05.000000",
        "progress=continue",
    ]

    for line in test_lines:
        result = parser.parse(line)

        if result is not None:
            progress = result

    assert progress is not None
    assert progress.frame == 100
    assert progress.time_seconds == 5.0

    print("\n=== PROGRESS WITH TIME ===")
    print(f"Frame: {progress.frame}")
    print(f"Time: {progress.time_seconds}")


if __name__ == "__main__":
    test_ffmpeg_progress_parser()
    test_ffmpeg_progress_with_time()