from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)


class HeaderWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(12)

        title = QLabel("R.I.T.M.O. Media Engine")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        version = QLabel("v1.0")
        version.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.active_library = QLabel("No library selected")
        self.active_library.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addStretch()
        layout.addWidget(self.active_library)

    def set_active_library(self, library_name: str) -> None:
        self.active_library.setText(library_name or "No library selected")
