from pathlib import Path

from modules.analyzer.analyzer import Analyzer
from modules.preferences.available_tracks_builder import (
    AvailableTracksBuilder,
)


def test_available_tracks_builder() -> None:
    file_path = (
        Path("data/samples")
        / "Frieren_S01E01_02m10s_02m30s_source.mp4"
    )

    analyzer = Analyzer()
    result = analyzer.analyze(file_path)

    assert result.success is True

    episode = type(
        "TestEpisode",
        (),
        {"media_item": result.media_item},
    )()

    builder = AvailableTracksBuilder()

    available_tracks = builder.build(
        [episode]
    )

    print("\n=== AVAILABLE AUDIO TRACKS ===")

    for track in available_tracks.audio_tracks:
        print(
            f"Stream: {track.stream_index} | "
            f"Language: {track.language.code} | "
            f"Title: {track.title} | "
            f"Default: {track.default} | "
            f"Forced: {track.forced}"
        )

    print("\n=== AVAILABLE SUBTITLE TRACKS ===")

    for track in available_tracks.subtitle_tracks:
        print(
            f"Stream: {track.stream_index} | "
            f"Language: {track.language.code} | "
            f"Title: {track.title} | "
            f"Default: {track.default} | "
            f"Forced: {track.forced}"
        )

    assert len(available_tracks.audio_tracks) == 3

    stream_indexes = [
        track.stream_index
        for track in available_tracks.audio_tracks
    ]

    assert stream_indexes == [1, 2, 3]


if __name__ == "__main__":
    test_available_tracks_builder()