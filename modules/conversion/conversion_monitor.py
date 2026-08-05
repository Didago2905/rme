from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, Signal


class ConversionMonitor(QObject):
    """
    Centraliza el monitoreo de una conversión.

    Responsabilidades:
    - Recibir líneas de salida de FFmpeg.
    - Emitirlas hacia la interfaz.
    - Guardarlas en un archivo de log.
    """

    log_received = Signal(str)

    def __init__(self, logs_directory: Path):
        super().__init__()

        self._logs_directory = logs_directory
        self._logs_directory.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self._log_file = (
            self._logs_directory /
            f"conversion_{timestamp}.log"
        )

    def append_log(self, line: str) -> None:

        line = line.rstrip()

        if not line:
            return

        with self._log_file.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(line + "\n")

        self.log_received.emit(line)

    @property
    def log_file(self) -> Path:
        return self._log_file