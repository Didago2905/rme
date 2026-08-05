from dataclasses import dataclass

from core.models.media_language import (
    MediaLanguage,
)


@dataclass(slots=True)
class SelectableLanguage:
    language: MediaLanguage

    selected: bool

    priority: int

    occurrences: int