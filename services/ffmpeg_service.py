from pathlib import Path
import json
import subprocess


class FFmpegService:
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
        )

        if result.returncode != 0:
            return {}

        return json.loads(result.stdout)