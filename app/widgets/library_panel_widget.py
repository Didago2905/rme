from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.themes.buttons import apply_primary_button


class LibraryPanelWidget(QWidget):
    scan_requested = Signal(str)
    import_series_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()
        self._update_action_buttons_state()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

    def _build_ui(self) -> None:
        """
        Construye el panel de biblioteca.
        """

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        self._build_header(main_layout)
        self._build_content(main_layout)

    def _build_header(self, layout: QVBoxLayout) -> None:
        """
        Construye el encabezado del panel.
        """

        title = QLabel("Library")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        layout.addWidget(title)
        layout.addWidget(separator)

    def _build_content(self, layout: QVBoxLayout) -> None:
        """
        Construye el contenido del panel.
        """

        folder_label = QLabel("Folder")

        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("Select a media library...")
        self.folder_path.setReadOnly(True)

        browse_button = QPushButton("Browse...")
        browse_button.setToolTip("Select a media library or series folder.")
        browse_button.clicked.connect(self._select_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(browse_button)

        self.scan_button = QPushButton("Scan Library")
        apply_primary_button(self.scan_button)
        self.scan_button.setToolTip("Analyze the selected media library.")
        self.scan_button.clicked.connect(self._scan_library)

        self.import_series_button = QPushButton("Import Series")
        apply_primary_button(self.import_series_button)
        self.import_series_button.setToolTip("Import a downloaded TV series.")
        self.import_series_button.clicked.connect(self._import_series)

        layout.addWidget(folder_label)
        layout.addLayout(folder_layout)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.import_series_button)

    def _select_folder(self) -> None:
        """
        Abre el selector de carpetas y actualiza la ruta seleccionada.
        """

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
        )

        if folder:
            self.folder_path.setText(folder)

        self._update_action_buttons_state()

    def _selected_path(self) -> str:
        """
        Devuelve la ruta actualmente seleccionada.
        """

        return self.folder_path.text().strip()

    def _update_action_buttons_state(self) -> None:
        """
        Actualiza el estado de los botones de acción.
        """

        has_folder = bool(self._selected_path())

        self.scan_button.setEnabled(has_folder)
        self.import_series_button.setEnabled(has_folder)

    def _scan_library(self) -> None:
        """
        Inicia el proceso de escaneo de la biblioteca.
        """

        library_path = self._selected_path()

        if not library_path:
            return

        self.scan_requested.emit(library_path)

    def _import_series(self) -> None:
        """
        Inicia el proceso de importación de una serie.
        """
        print("LibraryPanelWidget -> Import button pressed")

        series_path = self._selected_path()

        if not series_path:
            return

        self.import_series_requested.emit(series_path)
