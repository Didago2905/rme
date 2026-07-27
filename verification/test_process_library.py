from pathlib import Path

from modules.batch.batch_processor import BatchProcessor
from modules.batch.batch_report import BatchReport
from services.conversion_service import ConversionService


service = ConversionService()

processor = BatchProcessor(
    service
)

stats = processor.process_library(
    Path("data")
)

print(
    BatchReport.build(stats)
)