from pathlib import Path

from modules.analyzer.analyzer import Analyzer
from modules.validator.validator import Validator


def test_validator():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    analyzer = Analyzer()
    validator = Validator()

    analysis = analyzer.analyze(file_path)

    report = validator.validate(
        analysis.media_file
    )

    print(report)


if __name__ == "__main__":
    test_validator()