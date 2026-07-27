from pathlib import Path
from pprint import pprint

from services.ffmpeg_service import FFmpegService


def test_ffmpeg_service():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    service = FFmpegService()

    media_info = service.get_media_info(file_path)

    for stream in media_info["streams"]:
        if stream.get("codec_type") == "audio":
            pprint(stream)
            print()
            print("-" * 80)
            print()


if __name__ == "__main__":
    test_ffmpeg_service()