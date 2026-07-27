from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.models.media_file import MediaFile
from core.models.parsed_episode import ParsedEpisode
from core.models.season_metadata import SeasonMetadata
from core.models.series_metadata import SeriesMetadata
from modules.validation.validation_result import (
    ValidationResult,
)


class MediaInspectorWidget(QWidget):
    """
    Panel encargado de mostrar la información del elemento
    seleccionado en el árbol de importación.
    """

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(self) -> None:
        """
        Construye la interfaz del inspector.
        """

        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        self.title = QLabel("Media Inspector")
        self.title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.title)

        general_group = QGroupBox("General")
        general_layout = QFormLayout(general_group)

        self.type_value = QLabel("-")
        self.name_value = QLabel("-")
        self.seasons_value = QLabel("-")
        self.episodes_value = QLabel("-")
        self.file_name_value = QLabel("-")
        self.path_value = QLabel("-")
        self.path_value.setWordWrap(True)
        self.runtime_value = QLabel("Pending analysis...")

        general_layout.addRow("Type", self.type_value)
        general_layout.addRow("Name", self.name_value)
        general_layout.addRow("Season", self.seasons_value)
        general_layout.addRow("Episode", self.episodes_value)
        general_layout.addRow("File Name", self.file_name_value)
        general_layout.addRow("Path", self.path_value)
        general_layout.addRow("Runtime", self.runtime_value)

        content_layout.addWidget(general_group)

        technical_group = QGroupBox("Technical")
        technical_layout = QFormLayout(technical_group)

        self.analysis_value = QLabel("Not analyzed")
        self.analysis_value.setWordWrap(True)

        technical_layout.addRow("Details", self.analysis_value)

        content_layout.addWidget(technical_group)

        validation_group = QGroupBox("Validation")
        validation_layout = QFormLayout(validation_group)

        self.status_value = QLabel("Pending validation...")
        self.errors_value = QLabel("None")
        self.errors_value.setWordWrap(True)
        self.warnings_value = QLabel("None")
        self.warnings_value.setWordWrap(True)

        validation_layout.addRow("Status", self.status_value)
        validation_layout.addRow("Errors", self.errors_value)
        validation_layout.addRow("Warnings", self.warnings_value)

        content_layout.addWidget(validation_group)
        content_layout.addStretch()

        self.scroll_area.setWidget(content)
        layout.addWidget(self.scroll_area)

    def _clear_fields(self) -> None:
        """
        Restablece el contenido del inspector.
        """

        self.type_value.setText("-")
        self.name_value.setText("-")
        self.seasons_value.setText("-")
        self.episodes_value.setText("-")
        self.file_name_value.setText("-")
        self.path_value.setText("-")

        self.runtime_value.setText("Pending analysis...")

        self.analysis_value.setText("Not analyzed")

        self.status_value.setText("Pending validation...")

        self.errors_value.setText("None")

        self.warnings_value.setText("None")

    def show_item(
        self,
        item: object,
    ) -> None:
        """
        Muestra la información básica del
        elemento seleccionado.
        """

        self._clear_fields()

        if isinstance(
            item,
            SeriesMetadata,
        ):
            self._show_series(item)
            return

        if isinstance(
            item,
            SeasonMetadata,
        ):
            self._show_season(item)
            return

        if isinstance(
            item,
            ParsedEpisode,
        ):
            self.show_episode(item)
            return

        self.type_value.setText("Unknown")

    def _show_series(
        self,
        series: SeriesMetadata,
    ) -> None:
        """
        Muestra la información de una serie.
        """

        self.type_value.setText("Series")

        self.name_value.setText(series.name)

        self.seasons_value.setText(str(len(series.seasons)))

        total_episodes = sum(len(season.episodes) for season in series.seasons)

        self.episodes_value.setText(str(total_episodes))

    def _show_season(
        self,
        season: SeasonMetadata,
    ) -> None:
        """
        Muestra la información de una temporada.
        """

        self.type_value.setText("Season")

        self.name_value.setText(f"Season {season.season_number}")

        self.seasons_value.setText(str(season.season_number))

        self.episodes_value.setText(str(len(season.episodes)))

    def show_episode(
        self,
        episode: ParsedEpisode,
        media: Optional[MediaFile] = None,
        validation: Optional[ValidationResult] = None,
    ) -> None:
        """
        Muestra la información de un episodio.
        """

        self._clear_fields()

        self.type_value.setText("Episode")

        self.name_value.setText(
            (f"S{episode.season_number:02}E{episode.episode_number:02}")
        )

        self.seasons_value.setText(str(episode.season_number))

        self.episodes_value.setText(str(episode.episode_number))

        self.file_name_value.setText(episode.media_item.file_name)

        self.path_value.setText(str(episode.media_item.path))

        if media is None:
            return

        if not media.video_tracks:
            self.analysis_value.setText("No video tracks found.")
            return

        self.runtime_value.setText(self._format_duration(media.duration_seconds))

        video = media.video_tracks[0]

        analysis_text = (
            f"Codec: {video.codec}\n"
            f"Resolution: {video.width}x{video.height}\n"
            f"FPS: {video.frame_rate}\n"
            f"Pixel Format: {video.pixel_format}\n"
            f"Profile: {video.profile}\n"
            f"Level: {video.level}\n"
            f"Scan: {video.scan_type}"
        )

        self.analysis_value.setText(analysis_text)

        if validation is None:
            return

        if validation.is_valid:
            self.status_value.setText("✓ Compatible")
        else:
            self.status_value.setText("✗ Not Compatible")

        if validation.errors:
            self.errors_value.setText(
                "\n".join(f"• {error}" for error in validation.errors)
            )

        if validation.warnings:
            self.warnings_value.setText(
                "\n".join(f"• {warning}" for warning in validation.warnings)
            )

    def _format_duration(
        self,
        seconds: float,
    ) -> str:
        """
        Convierte una duración en segundos a un
        formato legible para el usuario.
        """

        total_seconds = int(seconds)

        hours = total_seconds // 3600

        minutes = (total_seconds % 3600) // 60

        remaining_seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}h {minutes:02}m {remaining_seconds:02}s"

        return f"{minutes}m {remaining_seconds:02}s"
