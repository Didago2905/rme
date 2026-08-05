from dataclasses import dataclass

from core.models.selectable_language import (
    SelectableLanguage,
)


@dataclass(slots=True)
class LanguagePreferences:
    audio_languages: list[SelectableLanguage]

    subtitle_languages: list[SelectableLanguage]