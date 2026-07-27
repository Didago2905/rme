from pathlib import Path

from modules.analyzer.analyzer import Analyzer
from modules.converter.converter import Converter
from modules.planner.planner import Planner
from modules.validator.validator import Validator


def test_converter():
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

    output_file = converter.build_output_file(
        file_path,
        job,
    )

    print()
    print(output_file)

    command = converter.build_command(
        file_path,
        job,
    )

    print()
    print(" ".join(command))


if __name__ == "__main__":
    test_converter()