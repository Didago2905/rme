from pathlib import Path

from PySide6.QtCore import Qt, QSettings, QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.use_cases.import_series_use_case import ImportSeriesUseCase
from app.use_cases.scan_library import ScanLibraryUseCase
from app.widgets.control_console_widget import ControlConsoleWidget
from app.widgets.header_widget import HeaderWidget
from app.widgets.import_preview_widget import ImportPreviewWidget
from app.widgets.library_panel_widget import LibraryPanelWidget
from core.models.parsed_episode import ParsedEpisode
from core.models.process_result import ProcessResult
from core.utils.media_library_name import build_episode_filename
from services.conversion_service import ConversionService
from core.models.ffmpeg_progress import FFmpegProgress
from app.widgets.conversion_setup_widget import (
    ConversionSetupWidget,
)


class ConversionWorker(QThread):
    result_ready = Signal(object, object)
    progress_updated = Signal(FFmpegProgress)

    def __init__(
        self,
        conversion_service: ConversionService,
        episode: ParsedEpisode,
        output_path: Path,
        conversion_settings: dict,
    ) -> None:
        super().__init__()
        self._conversion_service = conversion_service
        self._episode = episode
        self._output_path = output_path
        self._conversion_settings = conversion_settings

    def _on_progress(
        self,
        progress: FFmpegProgress,
    ) -> None:
        self.progress_updated.emit(progress)

    def run(self) -> None:
        try:
            result = self._conversion_service.process_file(
                file_path=self._episode.media_item.path,
                output_path=self._output_path,
                conversion_settings=(self._conversion_settings),
                on_progress=self._on_progress,
            )
        except Exception as error:
            result = ProcessResult(
                success=False,
                input_path=self._episode.media_item.path,
                output_path=self._output_path,
                error=str(error),
            )

        self.result_ready.emit(self._episode, result)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("R.I.T.M.O. Media Engine v1.0")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        self._conversion_worker: ConversionWorker | None = None
        self._active_series_name = ""
        self._settings = QSettings("RITMO", "RME")

        self._build_ui()

        self.scan_library_use_case = ScanLibraryUseCase()
        self.import_series_use_case = ImportSeriesUseCase()
        self.conversion_service = ConversionService()

        self.library_panel.set_media_library_path(
            self._settings.value(
                "media_library_path",
                "",
                type=str,
            )
        )

        self._connect_signals()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(12, 8, 12, 12)
        self.main_layout.setSpacing(10)

        self.header = HeaderWidget()
        self.library_panel = LibraryPanelWidget()
        self.import_preview = ImportPreviewWidget()
        self.control_console = ControlConsoleWidget()
        self.conversion_setup = ConversionSetupWidget()

        self.workspace = QSplitter(Qt.Orientation.Horizontal)
        self.workspace.setChildrenCollapsible(False)

        self.workspace.addWidget(self.import_preview)
        self.workspace.addWidget(self.conversion_setup)
        self.workspace.addWidget(self.control_console)

        self.workspace.setStretchFactor(0, 2)
        self.workspace.setStretchFactor(1, 2)
        self.workspace.setStretchFactor(2, 3)

        self.workspace.setSizes([320, 360, 520])

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.library_panel)
        self.main_layout.addWidget(
            self.workspace,
            1,
        )

    def _connect_signals(self) -> None:
        self.library_panel.scan_requested.connect(self._scan_library)

        self.library_panel.import_series_requested.connect(self._import_series)

        self.library_panel.media_library_changed.connect(self._save_media_library_path)

        self.import_preview.item_selected.connect(self._on_item_selected)

        self.import_preview.selection_changed.connect(self._on_selection_changed)

        self.import_preview.queue_requested.connect(self._add_selected_to_queue)

        self.control_console.start_requested.connect(self._start_queue)

    def _save_media_library_path(
        self,
        library_path: str,
    ) -> None:
        self._settings.setValue(
            "media_library_path",
            library_path,
        )

    def _scan_library(
        self,
        library_path: str,
    ) -> None:
        metadata = self.scan_library_use_case.execute(library_path)

        self.header.set_active_library(Path(library_path).name)

        print(metadata)

    def _import_series(
        self,
        series_path: str,
    ) -> None:
        metadata = self.import_series_use_case.execute(series_path)

        self._active_series_name = metadata.name

        self.header.set_active_library(metadata.name)

        self.import_preview.load_series(metadata)

    def _on_item_selected(
        self,
        item,
    ) -> None:
        selected = item.data(
            0,
            Qt.ItemDataRole.UserRole,
        )

        self.control_console.show_item(selected)

    def _on_selection_changed(
        self,
        episodes: list[ParsedEpisode],
    ) -> None:
        self.conversion_setup.load_selection(episodes)

    def _add_selected_to_queue(
        self,
        episodes: list[ParsedEpisode],
    ) -> None:
        media_library_path = self.library_panel.selected_media_library_path()

        if not media_library_path:
            self.control_console.show_library_destination_required()
            return

        output_paths = {
            episode.media_item.path: self._build_output_path(
                Path(media_library_path),
                episode,
            )
            for episode in episodes
        }

        self.control_console.add_episodes(
            episodes,
            output_paths,
        )

    def _build_output_path(
        self,
        media_library_path: Path,
        episode: ParsedEpisode,
    ) -> Path:

        series_name = (
            self._active_series_name or episode.media_item.path.parent.parent.name
        )

        filename = build_episode_filename(
            series_name,
            episode.season_number,
            episode.episode_number,
        )

        return (
            media_library_path
            / "Series"
            / series_name
            / f"Season {episode.season_number:02}"
            / filename
        )

    def _start_queue(self) -> None:

        if self._conversion_worker is not None:
            return

        episode = self.control_console.next_queued_episode()

        if episode is None:
            return

        output_path = self.control_console.output_path_for(episode)

        if output_path is None:
            return

        self.control_console.mark_running(episode)

        self._conversion_worker = ConversionWorker(
            self.conversion_service,
            episode,
            output_path,
            self.conversion_setup.conversion_settings(),
        )

        self._conversion_worker.result_ready.connect(self._on_conversion_finished)

        self._conversion_worker.progress_updated.connect(self._on_conversion_progress)

        self._conversion_worker.start()

    def _on_conversion_progress(
        self,
        progress: FFmpegProgress,
    ) -> None:

        if self._conversion_worker is None:
            return

        media_file = self._conversion_worker._episode.media_item

        self.control_console.update_conversion_progress(
            progress,
            media_file.total_frames,
            media_file.duration_formatted,
        )

    def _on_conversion_finished(
        self,
        episode: ParsedEpisode,
        result: ProcessResult,
    ) -> None:

        self.control_console.mark_result(
            episode,
            result,
        )

        if self._conversion_worker is not None:
            self._conversion_worker.deleteLater()
            self._conversion_worker = None

        if self.control_console.next_queued_episode() is not None:
            self._start_queue()
