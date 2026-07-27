from pathlib import Path

from core.models.analysis_result import AnalysisResult
from core.models.media_file import MediaFile


def test_analysis_result_creation():
    media = MediaFile(
        path=Path("Naruto.S01E01.mkv")
    )

    result = AnalysisResult(
        media_file=media,
        success=True,
        analyzer="ffprobe",
    )

    print(result)


if __name__ == "__main__":
    test_analysis_result_creation()