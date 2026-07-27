from pathlib import Path

from core.models.process_result import ProcessResult


result = ProcessResult(
    success=True,
    skipped=True,
    input_path=Path("video.mkv"),
    output_path=Path("video.mp4"),
)

print(result)