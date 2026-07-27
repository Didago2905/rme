from pathlib import Path

from services.conversion_service import ConversionService


service = ConversionService()

result = service.process_file(
    Path("data/samples/Samurai.Jack.2x01.HD720p-lat.mkv")
)

print()
print(result)