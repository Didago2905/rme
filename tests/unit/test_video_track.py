from core.models.video_track import VideoTrack


def test_video_track_creation():
    video = VideoTrack(
        codec="h264",
        width=1920,
        height=1080,
        bitrate=5000000,
        fps=23.976,
    )


    print(video)

if __name__ == "__main__":
    test_video_track_creation()
