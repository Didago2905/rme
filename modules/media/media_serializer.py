from core.models.media_file import (
    MediaFile,
)


def media_to_dict(
    media: MediaFile,
) -> dict:

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