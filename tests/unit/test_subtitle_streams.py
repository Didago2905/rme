from pathlib import Path

from services.ffmpeg_service import FFmpegService


def test_subtitle_streams():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    service = FFmpegService()

    media_info = service.get_media_info(
        file_path
    )

    for stream in media_info.get(
        "streams",
        []
    ):
        print(
            stream.get("index"),
            stream.get("codec_type"),
            stream.get("codec_name"),
        )


if __name__ == "__main__":
    test_subtitle_streams()