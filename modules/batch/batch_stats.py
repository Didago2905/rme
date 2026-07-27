from dataclasses import dataclass, field

from modules.batch.batch_result import BatchResult


@dataclass(slots=True)
class BatchStats:

    total_files: int = 0

    processed: int = 0

    skipped: int = 0

    failed: int = 0

    results: list[BatchResult] = field(
        default_factory=list
    )