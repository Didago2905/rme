import json
import subprocess
from pathlib import Path


class MediaProbe:

    def probe(
        self,
        media_path: Path,
    ) -> dict:

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(media_path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"FFprobe failed:\n{result.stderr}"
            )

        return json.loads(
            result.stdout
        )