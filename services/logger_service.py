from datetime import datetime
from pathlib import Path

from core.constants.paths import LOGS_DIR


class LoggerService:
    def __init__(self):
        LOGS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_file = (
            LOGS_DIR /
            "rme.log"
        )

    def info(
        self,
        message: str,
    ) -> None:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = (
            f"[INFO] "
            f"{timestamp} "
            f"{message}\n"
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(line)

    def error(
        self,
        message: str,
    ) -> None:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = (
            f"[ERROR] "
            f"{timestamp} "
            f"{message}\n"
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(line)