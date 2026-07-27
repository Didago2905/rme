from core.models.subtitle_track import SubtitleTrack


def test_subtitle_track_creation():
    subtitle = SubtitleTrack(
        codec="mov_text",
        language="spa",
        forced=False,
        default=True,
    )

    print(subtitle)


if __name__ == "__main__":
    test_subtitle_track_creation()