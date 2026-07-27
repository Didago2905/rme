from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QVBoxLayout,
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
        """
        Construye el contenido del encabezado.
        """

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("R.I.T.M.O. Media Engine")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Media Processing Suite")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("Version 0.1")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(version)