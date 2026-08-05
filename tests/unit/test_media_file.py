from core.models.audio_track import AudioTrack
from core.models.media_file import MediaFile
from core.models.subtitle_track import SubtitleTrack
from core.models.video_track import VideoTrack


def test_media_file_creation():
    media = MediaFile(
        container="mkv",
        duration_seconds=1338.336,
        size_bytes=123456789,
        bitrate=2500000,
        video_tracks=[
            VideoTrack(
                codec="h264",
                width=1920,
                height=1080,
                frame_rate="23.976",
                pixel_format="yuv420p",
                profile="High",
                level=4.1,
                scan_type="Progressive",
            )
        ],
        audio_tracks=[
            AudioTrack(
                codec="aac",
                channels=2,
                language="spa",
                title="Español Latino",
            )
        ],
        subtitle_tracks=[
            SubtitleTrack(
                codec="mov_text",
                language="spa",
                title="Español Latino",
            )
        ],
    )

    print(media)
    print(f"Duración: {media.duration_formatted}")
    print(f"Total de cuadros: {media.total_frames}")


if __name__ == "__main__":
    test_media_file_creation()