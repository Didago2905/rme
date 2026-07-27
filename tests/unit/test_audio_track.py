from core.models.audio_track import AudioTrack


def test_audio_track_creation():
    audio = AudioTrack(
        codec="aac",
        language="spa",
        channels=2,
        bitrate=192000,
    )

    print(audio)


if __name__ == "__main__":
    test_audio_track_creation()