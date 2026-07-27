from core.models.chapter import Chapter


def test_chapter_creation():
    chapter = Chapter(
        title="Opening",
        start_seconds=0.0,
        end_seconds=90.5,
    )

    print(chapter)


if __name__ == "__main__":
    test_chapter_creation()