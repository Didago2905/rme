from pathlib import Path
from shutil import copy2

from core.models.process_result import ProcessResult

from modules.conversion.conversion_job_builder import (
    ConversionJobBuilder,
)
from modules.converter.converter import Converter
from modules.media.media_service import MediaService
from modules.planning.conversion_planner import (
    ConversionPlanner,
)
from modules.validation.validation_service import (
    ValidationService,
)
from services.logger_service import LoggerService


class ConversionService:
    def __init__(self):
        self.media_service = MediaService()
        self.validation_service = ValidationService()
        self.conversion_planner = ConversionPlanner()
        self.conversion_job_builder = ConversionJobBuilder()
        self.converter = Converter()
        self.logger = LoggerService()

    def _is_output_valid(
        self,
        output_path: Path,
    ) -> bool:

        media = self.media_service.get_media(output_path)

        validation = self.validation_service.validate(media)

        return validation.is_valid

    def process_file(
        self,
        file_path: Path,
        output_path: Path | None = None,
    ) -> ProcessResult:

        self.logger.info(f"Processing file: {file_path.name}")

        media = self.media_service.get_media(file_path)

        validation = self.validation_service.validate(media)

        plan = self.conversion_planner.plan(
            media,
            validation,
        )

        if plan.compatible:
            self.logger.info(f"Already compatible: {file_path.name}")

            if output_path is not None and output_path != file_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)

                if not output_path.exists() or not self._is_output_valid(output_path):
                    copy2(file_path, output_path)

            return ProcessResult(
                success=True,
                skipped=True,
                input_path=file_path,
                output_path=output_path,
            )

        job = self.conversion_job_builder.build(
            media,
            plan,
        )

        output_file = self.converter.build_output_file(
            file_path,
            job,
            output_path,
        )

        if output_file.exists:
            self.logger.info(f"Output already exists: {output_file.output_path}")

            if self._is_output_valid(output_file.output_path):
                self.logger.info(f"Output already valid: {output_file.output_path}")

                print()
                print("OUTPUT ALREADY VALID")
                print(output_file.output_path)

                return ProcessResult(
                    success=True,
                    skipped=True,
                    input_path=file_path,
                    output_path=output_file.output_path,
                )

            self.logger.info(f"Output requires rebuild: {output_file.output_path}")

            print()
            print("OUTPUT EXISTS BUT IS NOT VALID")
            print(output_file.output_path)

        self.logger.info(f"Conversion job created: {job}")

        return_code = self.converter.execute(
            file_path,
            job,
            output_file.output_path,
        )

        if return_code == 0:
            if not self._is_output_valid(output_file.output_path):
                self.logger.error(
                    f"Output validation failed: {output_file.output_path.name}"
                )

                return ProcessResult(
                    success=False,
                    skipped=False,
                    input_path=file_path,
                    output_path=output_file.output_path,
                    error="Converted output failed WebSafe validation.",
                )

            self.logger.info(f"Conversion completed: {file_path.name}")

            return ProcessResult(
                success=True,
                skipped=False,
                input_path=file_path,
                output_path=output_file.output_path,
            )

        self.logger.error(f"Conversion failed: {file_path.name}")

        return ProcessResult(
            success=False,
            skipped=False,
            input_path=file_path,
            output_path=output_file.output_path,
            error=f"Return code: {return_code}",
        )
