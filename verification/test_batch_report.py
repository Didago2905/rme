from pathlib import Path

from modules.batch.batch_report import BatchReport
from modules.batch.batch_result import BatchResult
from modules.batch.batch_stats import BatchStats


stats = BatchStats(
    total_files=3,
    processed=1,
    skipped=1,
    failed=1,
)

stats.results.append(
    BatchResult(
        file_path=Path("episode01.mkv"),
        success=True,
    )
)

stats.results.append(
    BatchResult(
        file_path=Path("episode02.mkv"),
        success=True,
        skipped=True,
    )
)

stats.results.append(
    BatchResult(
        file_path=Path("episode03.mkv"),
        success=False,
        error="FFmpeg failed",
    )
)

report = BatchReport.build(
    stats
)

print(report)