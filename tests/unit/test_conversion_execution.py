from pathlib import Path

from modules.analyzer.analyzer import Analyzer
from modules.converter.converter import Converter
from modules.planner.planner import Planner
from modules.validator.validator import Validator


def test_conversion_execution():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    analyzer = Analyzer()
    validator = Validator()
    planner = Planner()
    converter = Converter()

    analysis = analyzer.analyze(file_path)

    report = validator.validate(
        analysis.media_file
    )

    job = planner.create_plan(
        report
    )

    return_code = converter.execute(
        file_path,
        job,
    )

    print()
    print("RETURN CODE")
    print(return_code)


if __name__ == "__main__":
    test_conversion_execution()