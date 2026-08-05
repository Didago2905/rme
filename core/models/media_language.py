from dataclasses import dataclass


@dataclass(slots=True)
class MediaLanguage:
    """
    ISO 639 language code
    detected in a media track.
    """

    code: str