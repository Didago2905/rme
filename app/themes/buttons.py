from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


PRIMARY_BUTTON = """
QPushButton {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}

QPushButton:hover {
    background-color: #1D4ED8;
}

QPushButton:pressed {
    background-color: #1E40AF;
}

QPushButton:disabled {
    background-color: #555555;
    color: #AAAAAA;
}
"""


def apply_primary_button(button: QPushButton) -> None:
    """
    Aplica el estilo del botón principal de RME.
    """

    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setStyleSheet(PRIMARY_BUTTON)
