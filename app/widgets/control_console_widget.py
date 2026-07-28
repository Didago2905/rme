from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.themes.buttons import apply_primary_button
from core.models.parsed_episode import ParsedEpisode
from core.models.process_result import ProcessResult
from core.models.season_metadata import SeasonMetadata
from core.models.series_metadata import SeriesMetadata


class ControlConsoleWidget(QWidget):
    start_requested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._queue: list[dict[str, object]] = []
        self._is_running = False
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        title = QLabel("Control Console")
        content_layout.addWidget(title)

        current_group = QGroupBox("Current Activity")
        current_layout = QFormLayout(current_group)
        self.activity_state = QLabel("Idle")
        self.current_item = QLabel("No conversion running")
        self.current_progress = QProgressBar()
        self.current_progress.setRange(0, 1)
        self.current_progress.setValue(0)
        current_layout.addRow("State", self.activity_state)
        current_layout.addRow("Item", self.current_item)
        current_layout.addRow("Current Item", self.current_progress)
        content_layout.addWidget(current_group)

        queue_group = QGroupBox("Queue")
        queue_layout = QVBoxLayout(queue_group)
        self.queue_list = QListWidget()
        self.queue_summary = QLabel("Empty queue")
        self.start_button = QPushButton("Start Queue")
        self.clear_button = QPushButton("Clear Queue")
        self.remove_selected_button = QPushButton("Remove Selected")
        apply_primary_button(self.start_button)
        self.start_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.remove_selected_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_requested.emit)
        self.clear_button.clicked.connect(self.clear_queue)
        self.remove_selected_button.clicked.connect(self.remove_selected)
        self.queue_list.itemSelectionChanged.connect(self._update_queue_actions_state)
        queue_layout.addWidget(self.queue_summary)
        queue_layout.addWidget(self.queue_list)
        queue_layout.addWidget(self.start_button)
        queue_layout.addWidget(self.remove_selected_button)
        queue_layout.addWidget(self.clear_button)
        content_layout.addWidget(queue_group)

        batch_group = QGroupBox("Batch Progress")
        batch_layout = QVBoxLayout(batch_group)
        self.segment_layout = QHBoxLayout()
        self.batch_progress = QProgressBar()
        self.batch_progress.setRange(0, 1)
        self.batch_progress.setValue(0)
        self.batch_progress.setFormat("0 / 0 processed")
        batch_layout.addLayout(self.segment_layout)
        batch_layout.addWidget(self.batch_progress)
        content_layout.addWidget(batch_group)

        selected_group = QGroupBox("Selected Item Summary")
        selected_layout = QFormLayout(selected_group)
        self.selected_type = QLabel("-")
        self.selected_name = QLabel("-")
        self.selected_file = QLabel("-")
        self.selected_path = QLabel("-")
        self.selected_path.setWordWrap(True)
        selected_layout.addRow("Type", self.selected_type)
        selected_layout.addRow("Name", self.selected_name)
        selected_layout.addRow("File", self.selected_file)
        selected_layout.addRow("Path", self.selected_path)
        content_layout.addWidget(selected_group)

        results_group = QGroupBox("Completed / Failed Summary")
        results_layout = QFormLayout(results_group)
        self.completed_summary = QLabel("0 completed")
        self.skipped_summary = QLabel("0 skipped")
        self.failed_summary = QLabel("0 failed")
        results_layout.addRow("Completed", self.completed_summary)
        results_layout.addRow("Skipped", self.skipped_summary)
        results_layout.addRow("Failed", self.failed_summary)
        content_layout.addWidget(results_group)
        content_layout.addStretch()

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

    def add_episodes(
        self,
        episodes: list[ParsedEpisode],
        output_paths: dict[Path, Path],
    ) -> None:
        queued_paths = {entry["path"] for entry in self._queue}

        for episode in episodes:
            path = episode.media_item.path

            if path not in queued_paths:
                self._queue.append(
                    {
                        "episode": episode,
                        "path": path,
                        "output_path": output_paths[path],
                        "state": "Queued",
                    }
                )
                queued_paths.add(path)

        self._refresh_queue()

    def next_queued_episode(self) -> ParsedEpisode | None:
        for entry in self._queue:
            if entry["state"] == "Queued":
                return entry["episode"]

        return None

    def output_path_for(self, episode: ParsedEpisode) -> Path | None:
        for entry in self._queue:
            if entry["path"] == episode.media_item.path:
                return entry["output_path"]

        return None

    def clear_queue(self) -> None:
        self._queue = [entry for entry in self._queue if entry["state"] != "Queued"]
        self._refresh_queue()

    def remove_selected(self) -> None:
        selected_paths = {
            item.data(Qt.ItemDataRole.UserRole)
            for item in self.queue_list.selectedItems()
        }
        self._queue = [
            entry
            for entry in self._queue
            if not (entry["path"] in selected_paths and entry["state"] == "Queued")
        ]
        self._refresh_queue()

    def mark_running(self, episode: ParsedEpisode) -> None:
        self._is_running = True
        self._set_state(episode, "Running")
        self.activity_state.setText("Running")
        self.current_item.setText(episode.media_item.file_name)
        self.current_progress.setRange(0, 0)
        self._refresh_queue()

    def mark_result(
        self,
        episode: ParsedEpisode,
        result: ProcessResult,
    ) -> None:
        if result.success and result.skipped:
            state = "Skipped"
        elif result.success:
            state = "Completed"
        else:
            state = "Failed"

        self._is_running = False
        self._set_state(episode, state)
        self.activity_state.setText(state)
        self.current_item.setText(episode.media_item.file_name)
        self.current_progress.setRange(0, 1)
        self.current_progress.setValue(1)
        self._refresh_queue()

    def show_library_destination_required(self) -> None:
        self.activity_state.setText("Idle")
        self.current_item.setText("Select a Media Library before adding to queue")

    def show_item(self, item: object) -> None:
        self._clear_selected_summary()

        if isinstance(item, SeriesMetadata):
            self.selected_type.setText("Series")
            self.selected_name.setText(item.name)
            return

        if isinstance(item, SeasonMetadata):
            self.selected_type.setText("Season")
            self.selected_name.setText(f"Season {item.season_number}")
            return

        if isinstance(item, ParsedEpisode):
            self.show_episode(item)

    def show_episode(self, episode: ParsedEpisode) -> None:
        self._clear_selected_summary()
        self.selected_type.setText("Episode")
        self.selected_name.setText(
            f"S{episode.season_number:02}E{episode.episode_number:02}"
        )
        self.selected_file.setText(episode.media_item.file_name)
        self.selected_path.setText(str(episode.media_item.path))

    def _clear_selected_summary(self) -> None:
        self.selected_type.setText("-")
        self.selected_name.setText("-")
        self.selected_file.setText("-")
        self.selected_path.setText("-")

    def _set_state(self, episode: ParsedEpisode, state: str) -> None:
        for entry in self._queue:
            if entry["path"] == episode.media_item.path:
                entry["state"] = state
                return

    def _refresh_queue(self) -> None:
        self.queue_list.clear()

        completed = 0
        skipped = 0
        failed = 0
        queued = 0

        for entry in self._queue:
            episode = entry["episode"]
            state = entry["state"]
            item = QListWidgetItem(f"{state} ? {episode.media_item.file_name}")
            item.setData(Qt.ItemDataRole.UserRole, entry["path"])
            self.queue_list.addItem(item)

            if state == "Completed":
                completed += 1
            elif state == "Skipped":
                skipped += 1
            elif state == "Failed":
                failed += 1
            elif state == "Queued":
                queued += 1

        total = len(self._queue)
        processed = completed + skipped + failed
        self.queue_summary.setText("Empty queue" if queued == 0 else f"{queued} queued")
        self.start_button.setEnabled(queued > 0 and not self._is_running)
        self.clear_button.setEnabled(queued > 0)
        self.batch_progress.setRange(0, max(total, 1))
        self.batch_progress.setValue(processed)
        self.batch_progress.setFormat(f"{processed} / {total} processed")
        self.completed_summary.setText(f"{completed} completed")
        self.skipped_summary.setText(f"{skipped} skipped")
        self.failed_summary.setText(f"{failed} failed")
        self._refresh_segments()
        self._update_queue_actions_state()

    def _update_queue_actions_state(self) -> None:
        has_queued_selection = any(
            self._state_for_path(item.data(Qt.ItemDataRole.UserRole)) == "Queued"
            for item in self.queue_list.selectedItems()
        )
        self.remove_selected_button.setEnabled(has_queued_selection)

    def _state_for_path(self, path: Path) -> str | None:
        for entry in self._queue:
            if entry["path"] == path:
                return entry["state"]

        return None

    def _refresh_segments(self) -> None:
        while self.segment_layout.count():
            item = self.segment_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        colors = {
            "Queued": "#6B7280",
            "Running": "#2563EB",
            "Completed": "#16A34A",
            "Skipped": "#D97706",
            "Failed": "#DC2626",
        }

        for entry in self._queue:
            segment = QLabel("?")
            segment.setStyleSheet(f"color: {colors[entry['state']]};")
            self.segment_layout.addWidget(segment)

        self.segment_layout.addStretch()
