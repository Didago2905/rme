from PySide6.QtWidgets import QPlainTextEdit


class ConversionConsole(QPlainTextEdit):
    """
    Consola de monitoreo de conversión.

    Responsabilidad:
    Mostrar las líneas recibidas del ConversionMonitor.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)

        self.setPlaceholderText(
            "Waiting for conversion..."
        )

    def append_log(self, line: str) -> None:
        self.appendPlainText(line)

        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(
            scrollbar.maximum()
        )

    def clear_console(self) -> None:
        self.clear()