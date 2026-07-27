from pathlib import Path

from modules.media.media_probe import (
    MediaProbe,
)

from modules.media.media_builder import (
    MediaBuilder,
)


def media_to_dict(media):

    return {
        "container": media.container,
        "duration_seconds": media.duration_seconds,
        "size_bytes": media.size_bytes,
        "bitrate": media.bitrate,
        "video_tracks": [
            {
                "codec": track.codec,
                "width": track.width,
                "height": track.height,
                "frame_rate": track.frame_rate,
            }
            for track in media.video_tracks
        ],
        "audio_tracks": [
            {
                "codec": track.codec,
                "channels": track.channels,
                "language": track.language,
                "title": track.title,
            }
            for track in media.audio_tracks
        ],
        "subtitle_tracks": [
            {
                "codec": track.codec,
                "language": track.language,
                "title": track.title,
            }
            for track in media.subtitle_tracks
        ],
    }


video_path = Path(
    r"D:\Media\TestLibrary\Malcolm In The Middle\Malcolm In The Middle  Temporada 1\Malcolm In The Middle  S01E01  .mkv"
)

probe = MediaProbe()

raw_data = probe.probe(
    video_path
)

media = MediaBuilder().build(
    raw_data
)

print(
    media_to_dict(media)
)