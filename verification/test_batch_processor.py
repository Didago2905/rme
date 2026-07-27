from pathlib import Path

from modules.batch.batch_processor import BatchProcessor
from services.conversion_service import ConversionService


service = ConversionService()

processor = BatchProcessor(service)

stats = processor.process_folder(
    Path("data/samples")
)

print()
print(stats)

print()
print("RESULTADOS")

for result in stats.results:
    print(result)