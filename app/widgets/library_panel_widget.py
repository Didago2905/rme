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
    media_library_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()
        self._update_action_buttons_state()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        self._build_header(main_layout)
        self._build_content(main_layout)

    def _build_header(self, layout: QVBoxLayout) -> None:
        title = QLabel("Library")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        layout.addWidget(title)
        layout.addWidget(separator)

    def _build_content(self, layout: QVBoxLayout) -> None:
        folder_label = QLabel("Source Folder")

        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("Select a media library or series...")
        self.folder_path.setReadOnly(True)

        browse_button = QPushButton("Browse...")
        browse_button.setToolTip("Select a media library or series folder.")
        browse_button.clicked.connect(self._select_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(browse_button)

        destination_label = QLabel("Streaming Media Root")
        self.media_library_path = QLineEdit()
        self.media_library_path.setPlaceholderText(
            "Select the Streaming App media root..."
        )
        self.media_library_path.setReadOnly(True)

        destination_button = QPushButton("Browse...")
        destination_button.setToolTip(
            "Select the Streaming App media root, for example D:\\Media."
        )
        destination_button.clicked.connect(self._select_media_library)

        destination_layout = QHBoxLayout()
        destination_layout.addWidget(self.media_library_path)
        destination_layout.addWidget(destination_button)

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
        layout.addWidget(destination_label)
        layout.addLayout(destination_layout)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.import_series_button)

    def set_media_library_path(self, path: str) -> None:
        self.media_library_path.setText(path)

    def selected_media_library_path(self) -> str:
        return self.media_library_path.text().strip()

    def _select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            self.folder_path.setText(folder)

        self._update_action_buttons_state()

    def _select_media_library(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Streaming Media Root")

        if folder:
            self.media_library_path.setText(folder)
            self.media_library_changed.emit(folder)

    def _selected_path(self) -> str:
        return self.folder_path.text().strip()

    def _update_action_buttons_state(self) -> None:
        has_folder = bool(self._selected_path())
        self.scan_button.setEnabled(has_folder)
        self.import_series_button.setEnabled(has_folder)

    def _scan_library(self) -> None:
        library_path = self._selected_path()

        if library_path:
            self.scan_requested.emit(library_path)

    def _import_series(self) -> None:
        series_path = self._selected_path()

        if series_path:
            self.import_series_requested.emit(series_path)
