"""
R.I.T.M.O. Media Engine (RME)

WebSafe Compatibility Specification v1

This file defines the minimum compatibility requirements for media files
that can be streamed without conversion.
"""

WEBSAFE_SPEC = {
    # Container
    "container": "mov,mp4,m4a,3gp,3g2,mj2",

    # Video
    "video_codec": "h264",

    "profiles": [
        "High",
    ],

    "pixel_formats": [
        "yuv420p",
    ],

    "max_level": 4.1,
    "max_width": 1920,
    "max_height": 1080,

    # Audio
    "audio_codecs": [
        "aac",
    ],
}