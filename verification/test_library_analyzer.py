from pathlib import Path

from modules.metadata.library_builder import (
    LibraryBuilder,
)

from modules.library.library_analyzer import (
    LibraryAnalyzer,
)


library = LibraryBuilder().build(
    Path(r"D:/Media/TestLibrary")
)

analyzer = LibraryAnalyzer()

stats = analyzer.analyze(
    library
)

print(stats)