from pathlib import Path
import json
import subprocess


class FFmpegService:

    def _subprocess_kwargs(self) -> dict:
        if subprocess.os.name != "nt":
            return {}

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        return {
            "startupinfo": startupinfo,
            "creationflags": subprocess.CREATE_NO_WINDOW,
        }

    def get_media_info(self, file_path: Path) -> dict:
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            **self._subprocess_kwargs(),
        )

        if result.returncode != 0:
            return {}

        return json.loads(result.stdout)