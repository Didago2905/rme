from typing import Optional


def normalize_video_level(
    codec: str,
    raw_level: Optional[int],
) -> Optional[float]:
    """
    Normalize FFprobe video level values into a common representation.

    Examples:
        H264:
            40 -> 4.0
            41 -> 4.1
            42 -> 4.2

        HEVC:
            120 -> 4.0
            123 -> 4.1
            150 -> 5.0
    """

    if raw_level is None:
        return None

    codec = codec.lower()

    if codec in ("h264", "avc"):
        return raw_level / 10

    if codec in ("hevc", "h265"):
        return raw_level / 30

    return None