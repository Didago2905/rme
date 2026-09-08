from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.models.media_item import MediaItem
from core.models.parsed_episode import ParsedEpisode
from core.models.series_metadata import SeriesMetadata


class ImportPreviewWidget(QWidget):

    item_selected = Signal(QTreeWidgetItem)

    selection_changed = Signal(object)

    queue_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(8)

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels(
            ["Library"]
        )

        self.tree.setMinimumWidth(0)

        self.tree.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.setMinimumWidth(250)

        layout.addWidget(
            self.tree
        )

        self.add_to_queue_button = QPushButton(
            "Add to Queue"
        )

        self.add_to_queue_button.setEnabled(
            False
        )

        layout.addWidget(
            self.add_to_queue_button
        )

    def _connect_signals(self) -> None:

        self.tree.itemSelectionChanged.connect(
            self._on_selection_changed
        )

        self.tree.itemChanged.connect(
            self._on_item_changed
        )

        self.add_to_queue_button.clicked.connect(
            self._request_queue
        )

    def _update_queue_button(
        self,
        has_selection: bool,
    ) -> None:

        self.add_to_queue_button.setEnabled(
            has_selection
        )

        if has_selection:

            self.add_to_queue_button.setStyleSheet(
                "background-color: #1976D2;"
            )

        else:

            self.add_to_queue_button.setStyleSheet(
                ""
            )

    def reset_queue_button(
        self,
    ) -> None:

        self._update_queue_button(
            False
        )

    def _on_selection_changed(self) -> None:

        item = self.tree.currentItem()

        if item is not None:
            self.item_selected.emit(item)

    def _on_item_changed(
        self,
        item: QTreeWidgetItem,
        column: int,
    ) -> None:

        episodes = self.selected_items()

        self.selection_changed.emit(
            episodes
        )

        self._update_queue_button(
            bool(episodes)
        )

    def _request_queue(
        self,
    ) -> None:

        self.queue_requested.emit(
            self.selected_items()
        )

    def selected_items(
        self,
    ) -> list[ParsedEpisode | MediaItem]:

        episodes = []

        def collect(
            item: QTreeWidgetItem,
        ) -> None:

            selected = item.data(
                0,
                Qt.ItemDataRole.UserRole,
            )

            if (
                isinstance(
                    selected,
                    (ParsedEpisode, MediaItem),
                )
                and item.checkState(0)
                == Qt.CheckState.Checked
            ):
                episodes.append(selected)

            for index in range(
                item.childCount()
            ):
                collect(
                    item.child(index)
                )

        for index in range(
            self.tree.topLevelItemCount()
        ):
            collect(
                self.tree.topLevelItem(index)
            )

        return episodes

    def load_series(
        self,
        metadata: SeriesMetadata,
    ) -> None:

        self.tree.blockSignals(True)

        self.tree.clear()

        root = self._create_item(
            metadata.name,
            metadata,
            tri_state=True,
        )

        self.tree.addTopLevelItem(root)

        for season in metadata.seasons:

            if season.season_number is None:

                season_label = "Season ?"

            else:

                season_label = (
                    f"Season {season.season_number}"
                )

            season_item = self._create_item(
                season_label,
                season,
                tri_state=True,
            )

            root.addChild(
                season_item
            )

            for episode in season.episodes:

                if (
                    episode.season_number is not None
                    and episode.episode_number is not None
                ):

                    episode_label = (
                        f"S{episode.season_number:02}"
                        f"E{episode.episode_number:02}"
                    )

                else:

                    episode_label = (
                        "Unnumbered - "
                        f"{episode.media_item.file_name}"
                    )

                episode_item = self._create_item(
                    episode_label,
                    episode,
                )

                season_item.addChild(
                    episode_item
                )

            season_item.setExpanded(False)

        root.setExpanded(True)

        self.tree.blockSignals(False)

        self._update_queue_button(
            False
        )

    def load_movie(
        self,
        media_item: MediaItem,
    ) -> None:
        self.tree.blockSignals(True)
        self.tree.clear()
        self.tree.addTopLevelItem(
            self._create_item(media_item.path.parent.name, media_item)
        )
        self.tree.blockSignals(False)
        self._update_queue_button(False)

    def _create_item(
        self,
        label: str,
        value: object,
        tri_state: bool = False,
    ) -> QTreeWidgetItem:

        item = QTreeWidgetItem([label])

        flags = (
            item.flags()
            | Qt.ItemFlag.ItemIsUserCheckable
        )

        if tri_state:

            flags |= (
                Qt.ItemFlag.ItemIsAutoTristate
            )

        item.setFlags(flags)

        item.setCheckState(
            0,
            Qt.CheckState.Unchecked,
        )

        item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            value,
        )

        return item