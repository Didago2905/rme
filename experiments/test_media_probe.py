import json
import subprocess
from pathlib import Path


VIDEO_FILE = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

result = subprocess.run(
    [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(VIDEO_FILE),
    ],
    capture_output=True,
    text=True,
)

data = json.loads(result.stdout)

print("\n==============================")
print("FORMAT")
print("==============================")

format_info = data.get("format", {})

print(f"Container : {format_info.get('format_name')}")
print(f"Duration  : {format_info.get('duration')}")
print(f"Size      : {format_info.get('size')}")
print(f"Bitrate   : {format_info.get('bit_rate')}")

print("\n==============================")
print("STREAMS")
print("==============================")

for stream in data.get("streams", []):

    codec_type = stream.get("codec_type")

    print("\n------------------------------")
    print(f"TYPE : {codec_type}")

    if codec_type == "video":

        print(f"Codec      : {stream.get('codec_name')}")
        print(f"Width      : {stream.get('width')}")
        print(f"Height     : {stream.get('height')}")
        print(f"Frame Rate : {stream.get('r_frame_rate')}")

    elif codec_type == "audio":

        tags = stream.get("tags", {})

        print(f"Codec      : {stream.get('codec_name')}")
        print(f"Channels   : {stream.get('channels')}")
        print(f"Language   : {tags.get('language')}")
        print(f"Title      : {tags.get('title')}")

    elif codec_type == "subtitle":

        tags = stream.get("tags", {})

        print(f"Codec      : {stream.get('codec_name')}")
        print(f"Language   : {tags.get('language')}")
        print(f"Title      : {tags.get('title')}")