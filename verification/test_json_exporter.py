from pathlib import Path

from modules.metadata.library_builder import (
    LibraryBuilder,
)

from core.exporters.json_exporter import (
    JsonExporter,
)


library = LibraryBuilder().build(
    Path(r"D:/Media/TestLibrary")
)

JsonExporter.export_library(
    library,
    Path("output/library.json"),
)

print("JSON generado correctamente")