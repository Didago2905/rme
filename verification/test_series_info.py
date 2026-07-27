from pathlib import Path

from core.models.series_info import SeriesInfo


series = SeriesInfo(
    name="Samurai Jack",
    path=Path("D:/Media/Series/Samurai Jack"),
)

print(series)