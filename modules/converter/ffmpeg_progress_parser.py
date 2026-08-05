from core.models.ffmpeg_progress import FFmpegProgress


class FFmpegProgressParser:
    def __init__(self) -> None:
        self._frame: int | None = None
        self._time_seconds: float | None = None

    def parse(
        self,
        line: str,
    ) -> FFmpegProgress | None:

        if "=" not in line:
            return None

        key, value = line.split("=", 1)

        if key == "frame":

            if not value.isdigit():
                return None

            self._frame = int(value)

        elif key == "out_time_ms":

            if not value.isdigit():
                return None

            self._time_seconds = int(value) / 1_000_000

        elif key == "progress":

            if (
                self._frame is None
                or self._time_seconds is None
            ):
                return None

            return FFmpegProgress(
                frame=self._frame,
                time_seconds=self._time_seconds,
            )

        return None