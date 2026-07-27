from pathlib import Path

from modules.analyzer.analyzer import Analyzer
from modules.planner.planner import Planner
from modules.validator.validator import Validator


def test_planner():
    sample_dir = Path("data/samples")

    file_path = next(sample_dir.iterdir())

    analyzer = Analyzer()
    validator = Validator()
    planner = Planner()

    analysis = analyzer.analyze(file_path)

    report = validator.validate(
        analysis.media_file
    )

    job = planner.create_plan(
        report
    )

    print(job)


if __name__ == "__main__":
    test_planner()