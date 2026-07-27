from pathlib import Path

from modules.metadata.metadata_builder import (
    MetadataBuilder,
)


builder = MetadataBuilder()

metadata = builder.build(
    Path("data/samples")
)

print()

print(metadata)