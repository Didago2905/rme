from pathlib import Path

from core.models.process_result import ProcessResult

from modules.analyzer.analyzer import Analyzer
from modules.converter.converter import Converter
from modules.planner.planner import Planner
from modules.validator.validator import Validator

from services.logger_service import LoggerService


class ConversionService:

    def __init__(self):
        self.analyzer = Analyzer()
        self.validator = Validator()
        self.planner = Planner()
        self.converter = Converter()
        self.logger = LoggerService()

    def _is_output_valid(
        self,
        output_path: Path,
    ) -> bool:

        analysis = self.analyzer.analyze(
            output_path
        )

        report = self.validator.validate(
            analysis.media_file
        )

        return report.is_compatible

    def process_file(
        self,
        file_path: Path,
    ) -> ProcessResult:

        self.logger.info(
            f"Processing file: {file_path.name}"
        )

        analysis = self.analyzer.analyze(
            file_path
        )

        report = self.validator.validate(
            analysis.media_file
        )

        job = self.planner.create_plan(
            report
        )

        output_file = self.converter.build_output_file(
            file_path,
            job,
        )

        if output_file.exists:

            self.logger.info(
                f"Output already exists: "
                f"{output_file.output_path}"
            )

            if self._is_output_valid(
                output_file.output_path
            ):

                self.logger.info(
                    f"Output already valid: "
                    f"{output_file.output_path}"
                )

                print()
                print("OUTPUT ALREADY VALID")
                print(output_file.output_path)

                return ProcessResult(
                    success=True,
                    skipped=True,
                    input_path=file_path,
                    output_path=output_file.output_path,
                )

            self.logger.info(
                f"Output requires rebuild: "
                f"{output_file.output_path}"
            )

            print()
            print("OUTPUT EXISTS BUT IS NOT VALID")
            print(output_file.output_path)

        self.logger.info(
            f"Conversion job created: {job}"
        )

        return_code = self.converter.execute(
            file_path,
            job,
        )

        if return_code == 0:

            self.logger.info(
                f"Conversion completed: {file_path.name}"
            )

            return ProcessResult(
                success=True,
                skipped=False,
                input_path=file_path,
                output_path=output_file.output_path,
            )

        self.logger.error(
            f"Conversion failed: {file_path.name}"
        )

        return ProcessResult(
            success=False,
            skipped=False,
            input_path=file_path,
            output_path=output_file.output_path,
            error=f"Return code: {return_code}",
        )