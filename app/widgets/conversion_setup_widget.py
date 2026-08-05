from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from core.models.parsed_episode import (
    ParsedEpisode,
)

from modules.preferences.available_tracks_builder import (
    AvailableTracksBuilder,
)


class ConversionSetupWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._tracks_builder = (
            AvailableTracksBuilder()
        )

        self._audio_checkboxes = []

        self._subtitle_checkboxes = []

        self._audio_group = (
            QButtonGroup(self)
        )

        self._build_ui()

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(8)

        self.panel = QFrame()

        panel_layout = QVBoxLayout(
            self.panel
        )

        self.title = QLabel(
            "Conversion Setup"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.series_label = QLabel()

        self.selection_label = QLabel()

        self.episodes_label = QLabel()

        self.audio_title = QLabel(
            "Available Audio"
        )

        self.audio_layout = QVBoxLayout()

        self.subtitle_title = QLabel(
            "Available Subtitles"
        )

        self.subtitle_layout = (
            QVBoxLayout()
        )

        self.summary = QLabel(
            "Nothing selected."
        )

        self.summary.setWordWrap(True)

        panel_layout.addWidget(
            self.title
        )

        panel_layout.addWidget(
            self.summary
        )

        panel_layout.addWidget(
            self.series_label
        )

        panel_layout.addWidget(
            self.selection_label
        )

        panel_layout.addWidget(
            self.episodes_label
        )

        panel_layout.addSpacing(12)

        panel_layout.addWidget(
            self.audio_title
        )

        panel_layout.addLayout(
            self.audio_layout
        )

        panel_layout.addSpacing(8)

        panel_layout.addWidget(
            self.subtitle_title
        )

        panel_layout.addLayout(
            self.subtitle_layout
        )

        panel_layout.addStretch()

        layout.addWidget(
            self.panel
        )

    def load_selection(
        self,
        episodes: list[ParsedEpisode],
    ) -> None:

        self._clear_language_lists()

        if not episodes:

            self.summary.setText(
                "Nothing selected."
            )

            self.series_label.clear()

            self.selection_label.clear()

            self.episodes_label.clear()

            return

        available_tracks = (
            self._tracks_builder.build(
                episodes
            )
        )

        series_name = (
            episodes[0]
            .media_item
            .path
            .parent
            .parent
            .name
        )

        seasons = sorted(
            {
                episode.season_number
                for episode in episodes
            }
        )

        count = len(episodes)

        self.summary.clear()

        self.series_label.setText(
            f"Series: {series_name}"
        )

        if count == 1:

            episode = episodes[0]

            self.selection_label.setText(
                (
                    "Selection: "
                    f"S{episode.season_number:02}"
                    f"E{episode.episode_number:02}"
                )
            )

        elif len(seasons) == 1:

            self.selection_label.setText(
                (
                    "Selection: "
                    f"Season {seasons[0]}"
                )
            )

        else:

            first = seasons[0]

            last = seasons[-1]

            consecutive = (
                seasons
                == list(
                    range(
                        first,
                        last + 1,
                    )
                )
            )

            if consecutive:

                selection = (
                    f"Season {first}–{last}"
                )

            else:

                selection = (
                    "Season "
                    + ", ".join(
                        str(season)
                        for season in seasons
                    )
                )

            self.selection_label.setText(
                f"Selection: {selection}"
            )

        self.episodes_label.setText(
            f"Episodes: {count}"
        )

        #
        # AUDIO
        #

        for index, language in enumerate(
            available_tracks.audio_languages
        ):

            row = QHBoxLayout()

            checkbox = QCheckBox(
                language.code.upper()
            )

            checkbox.setChecked(True)

            radio = QRadioButton()

            if index == 0:

                radio.setChecked(True)

            self._audio_group.addButton(
                radio
            )

            row.addWidget(
                checkbox
            )

            row.addStretch()

            row.addWidget(
                radio
            )

            self.audio_layout.addLayout(
                row
            )

            self._audio_checkboxes.append(
                checkbox
            )

        if not self._audio_checkboxes:

            self.audio_layout.addWidget(
                QLabel("None")
            )

        #
        # SUBTITLES
        #

        for language in (
            available_tracks.subtitle_languages
        ):

            checkbox = QCheckBox(
                language.code.upper()
            )

            checkbox.setChecked(True)

            self.subtitle_layout.addWidget(
                checkbox
            )

            self._subtitle_checkboxes.append(
                checkbox
            )

        if not self._subtitle_checkboxes:

            self.subtitle_layout.addWidget(
                QLabel("None")
            )

    def _clear_language_lists(
        self,
    ) -> None:

        while self.audio_layout.count():

            item = self.audio_layout.takeAt(
                0
            )

            if item.layout():

                while item.layout().count():

                    child = (
                        item.layout().takeAt(0)
                    )

                    widget = child.widget()

                    if widget is not None:

                        widget.deleteLater()

                del item

            else:

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

        while self.subtitle_layout.count():

            item = (
                self.subtitle_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        self._audio_group = (
            QButtonGroup(self)
        )

        self._audio_checkboxes.clear()

        self._subtitle_checkboxes.clear()

    def conversion_settings(
        self,
    ) -> dict:

        default_audio = None

        for checkbox, radio in zip(
            self._audio_checkboxes,
            self._audio_group.buttons(),
        ):

            if radio.isChecked():

                default_audio = (
                    checkbox.text().lower()
                )

                break

        return {
            "audio": [
                checkbox.text().lower()
                for checkbox in self._audio_checkboxes
                if checkbox.isChecked()
        ],
        "subtitles": [
            checkbox.text().lower()
            for checkbox in self._subtitle_checkboxes
            if checkbox.isChecked()
        ],
        "default_audio": default_audio,
    }