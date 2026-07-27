from core.models.conversion_profile import ConversionProfile


def test_conversion_profile_creation():
    profile = ConversionProfile(
        name="web_safe",
        video_codec="h264",
        audio_codec="aac",
        subtitle_codec="mov_text",
        allowed_containers=["mp4"],
    )

    print(profile)


if __name__ == "__main__":
    test_conversion_profile_creation()