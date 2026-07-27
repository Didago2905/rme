from pathlib import Path

from core.models.audio_track import AudioTrack
from core.models.chapter import Chapter
from core.models.media_file import MediaFile
from core.models.subtitle_track import SubtitleTrack
from core.models.video_track import VideoTrack


def test_media_file_creation():
    media = MediaFile(
        path=Path("Naruto.S01E01.mkv"),
        file_name="Naruto.S01E01.mkv",
        container="mkv",
        video_tracks=[
            VideoTrack(codec="h264")
        ],
        audio_tracks=[
            AudioTrack(codec="aac", language="spa")
        ],
        subtitle_tracks=[
            SubtitleTrack(codec="mov_text", language="spa")
        ],
        chapters=[
            Chapter(title="Opening")
        ],
    )

    print(media)


if __name__ == "__main__":
    test_media_file_creation()