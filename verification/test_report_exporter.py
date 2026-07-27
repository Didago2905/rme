from pathlib import Path

from modules.metadata.library_builder import (
    LibraryBuilder,
)

from core.exporters.report_exporter import (
    ReportExporter,
)


library = LibraryBuilder().build(
    Path(r"D:/Media/TestLibrary")
)

ReportExporter.export_library(
    library,
    Path("output/library_report.txt"),
)

print("REPORTE GENERADO CORRECTAMENTE")