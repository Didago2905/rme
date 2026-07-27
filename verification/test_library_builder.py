from pathlib import Path

from modules.metadata.library_builder import (
    LibraryBuilder,
)


builder = LibraryBuilder()

library = builder.build(
    Path("D:/Media/TestLibrary")
)

print()

print(library)