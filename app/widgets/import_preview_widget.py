from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.models.series_metadata import (
    SeriesMetadata,
)


class ImportPreviewWidget(QWidget):

    #
    # Se emite cuando cambia el elemento
    # seleccionado en el árbol.
    #
    item_selected = Signal(QTreeWidgetItem)

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

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels(
            ["Library"]
        )

        #
        # Permite que el árbol se adapte
        # correctamente al QSplitter.
        #
        self.tree.setMinimumWidth(0)

        self.tree.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self.setMinimumWidth(250)

        layout.addWidget(
            self.tree
        )

    def _connect_signals(self) -> None:
        """
        Conecta las señales internas del árbol.
        """

        self.tree.itemSelectionChanged.connect(
            self._on_selection_changed
        )

    def _on_selection_changed(self) -> None:
        """
        Notifica cuando cambia la selección.
        """

        item = self.tree.currentItem()

        if item is None:
            return

        self.item_selected.emit(
            item
        )

    def load_series(
        self,
        metadata: SeriesMetadata,
    ) -> None:
        """
        Muestra una serie en el árbol.
        """

        self.tree.clear()

        root = QTreeWidgetItem(
            [
                metadata.name
            ]
        )

        #
        # Asociar el objeto del dominio.
        #
        root.setData(
            0,
            Qt.UserRole,
            metadata,
        )

        self.tree.addTopLevelItem(
            root
        )

        for season in metadata.seasons:

            season_item = QTreeWidgetItem(
                [
                    f"Season {season.season_number}"
                ]
            )

            #
            # Asociar el objeto del dominio.
            #
            season_item.setData(
                0,
                Qt.UserRole,
                season,
            )

            root.addChild(
                season_item
            )

            for episode in season.episodes:

                episode_item = QTreeWidgetItem(
                    [
                        (
                            f"S{episode.season_number:02}"
                            f"E{episode.episode_number:02}"
                        )
                    ]
                )

                #
                # Asociar el objeto del dominio.
                #
                episode_item.setData(
                    0,
                    Qt.UserRole,
                    episode,
                )

                season_item.addChild(
                    episode_item
                )

            #
            # Las temporadas nacen contraídas.
            #
            season_item.setExpanded(
                False
            )

        #
        # La serie permanece expandida
        # para mostrar únicamente las
        # temporadas.
        #
        root.setExpanded(
            True
        )