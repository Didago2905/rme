from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.themes.buttons import apply_primary_button
from core.models.parsed_episode import ParsedEpisode
from core.models.series_metadata import SeriesMetadata


class ImportPreviewWidget(QWidget):
    item_selected = Signal(QTreeWidgetItem)
    queue_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Library"])
        self.tree.setMinimumWidth(0)
        self.tree.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.add_to_queue_button = QPushButton("Add Selected to Queue")
        apply_primary_button(self.add_to_queue_button)
        self.add_to_queue_button.setEnabled(False)
        self.add_to_queue_button.setToolTip(
            "Add checked episodes to the conversion queue."
        )

        self.setMinimumWidth(250)

        layout.addWidget(self.tree)
        layout.addWidget(self.add_to_queue_button)

    def _connect_signals(self) -> None:
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemChanged.connect(self._update_queue_action_state)
        self.add_to_queue_button.clicked.connect(self._request_queue)

    def _on_selection_changed(self) -> None:
        item = self.tree.currentItem()

        if item is not None:
            self.item_selected.emit(item)

    def _update_queue_action_state(self, item=None, column=0) -> None:
        self.add_to_queue_button.setEnabled(bool(self.selected_episodes()))

    def _request_queue(self) -> None:
        episodes = self.selected_episodes()

        if episodes:
            self.queue_requested.emit(episodes)

    def selected_episodes(self) -> list[ParsedEpisode]:
        episodes = []

        def collect(item: QTreeWidgetItem) -> None:
            selected = item.data(0, Qt.ItemDataRole.UserRole)

            if (
                isinstance(selected, ParsedEpisode)
                and item.checkState(0) == Qt.CheckState.Checked
            ):
                episodes.append(selected)

            for index in range(item.childCount()):
                collect(item.child(index))

        for index in range(self.tree.topLevelItemCount()):
            collect(self.tree.topLevelItem(index))

        return episodes

    def load_series(self, metadata: SeriesMetadata) -> None:
        self.tree.blockSignals(True)
        self.tree.clear()

        root = self._create_item(metadata.name, metadata, tri_state=True)
        self.tree.addTopLevelItem(root)

        for season in metadata.seasons:
            season_item = self._create_item(
                f"Season {season.season_number}",
                season,
                tri_state=True,
            )
            root.addChild(season_item)

            for episode in season.episodes:
                episode_item = self._create_item(
                    f"S{episode.season_number:02}E{episode.episode_number:02}",
                    episode,
                )
                season_item.addChild(episode_item)

            season_item.setExpanded(False)

        root.setExpanded(True)
        self.tree.blockSignals(False)
        self._update_queue_action_state()

    def _create_item(
        self,
        label: str,
        value: object,
        tri_state: bool = False,
    ) -> QTreeWidgetItem:
        item = QTreeWidgetItem([label])
        flags = item.flags() | Qt.ItemFlag.ItemIsUserCheckable

        if tri_state:
            flags |= Qt.ItemFlag.ItemIsAutoTristate

        item.setFlags(flags)
        item.setCheckState(0, Qt.CheckState.Unchecked)
        item.setData(0, Qt.ItemDataRole.UserRole, value)

        return item
