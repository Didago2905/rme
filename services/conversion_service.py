from pathlib import Path
from shutil import copy2

from core.constants.paths import LOGS_DIR
from core.models.process_result import ProcessResult
from core.models.conversion_job import ConversionJob
from core.models.media_item import MediaItem
from modules.validation.output_verifier import OutputVerifier
from modules.validation.validation_result import ValidationResult

from modules.conversion.conversion_job_builder import (
    ConversionJobBuilder,
)
from modules.conversion.conversion_monitor import ConversionMonitor
from modules.converter.converter import Converter
from modules.media.media_service import MediaService
from modules.planning.conversion_planner import (
    ConversionPlanner,
)
from modules.validation.validation_service import (
    ValidationService,
)
from services.logger_service import LoggerService
from core.models.ffmpeg_progress import FFmpegProgress
from typing import Callable


class ConversionService:
    def __init__(self):
        self.media_service = MediaService()
        self.validation_service = ValidationService()
        self.output_verifier = OutputVerifier()
        self.conversion_planner = ConversionPlanner()
        self.conversion_job_builder = ConversionJobBuilder()
        self.converter = Converter()
        self.logger = LoggerService() 

    def _validate_output(
        self, source: MediaItem, output_path: Path, job: ConversionJob,
    ) -> ValidationResult:
        try:
            if not output_path.is_file() or output_path.stat().st_size == 0:
                return ValidationResult(False, ["Output file is missing or empty."])
            output = self.media_service.get_media(output_path)
            verification = self.output_verifier.verify(source, output, job)
        except Exception as error:
            return ValidationResult(False, [f"Output verification failed: {error}"])

        if not verification.is_valid:
            return verification
        return self.validation_service.validate(output)

    def process_file(
        self,
        file_path: Path,
        output_path: Path | None = None,
        conversion_settings: dict | None = None,
        on_progress: Callable[[FFmpegProgress], None] | None = None,
            
    ) -> ProcessResult:

        self.logger.info(f"Processing file: {file_path.name}")
        print("1 - process_file")

        media = self.media_service.get_media(file_path)
        print("2 - media loaded")

        validation = self.validation_service.validate(media)
        print("3 - validation")

        plan = self.conversion_planner.plan(
            media,
            validation,
        )

        print("4 - planning")

        if plan.compatible:
            self.logger.info(f"Already compatible: {file_path.name}")
            destination = output_path if output_path is not None else file_path
            # A byte-for-byte copy must retain all source tracks, even when
            # the conversion settings select only a subset.
            copy_job = ConversionJob(
                audio_tracks=media.audio_tracks,
                include_subtitles=bool(media.subtitle_tracks),
                subtitle_tracks=media.subtitle_tracks,
            )
            if destination != file_path:
                destination.parent.mkdir(parents=True, exist_ok=True)
                existing = self._validate_output(media, destination, copy_job)
                if not existing.is_valid:
                    self.logger.info(
                        f"Output requires copy: {destination} - "
                        + "; ".join(existing.errors)
                    )
                    try:
                        copy2(file_path, destination)
                    except Exception as error:
                        self.logger.error(f"Copy failed: {destination} - {error}")
                        return ProcessResult(
                            success=False, input_path=file_path,
                            output_path=destination, error=str(error),
                        )

            checked = self._validate_output(media, destination, copy_job)
            if not checked.is_valid:
                self.logger.error(
                    f"Output validation failed: {destination} - "
                    + "; ".join(checked.errors)
                )
            return ProcessResult(
                success=checked.is_valid,
                skipped=checked.is_valid,
                input_path=file_path,
                output_path=output_path,
                error="\n".join(checked.errors) or None,
            )

        try:
            print("5 - building job")
            job = self.conversion_job_builder.build(
                media,
                plan,
                conversion_settings,
            )
            print("6 - job created")
        except Exception as e:
            self.logger.error(
                f"Failed to build conversion job: {file_path.name} - {e}"
            )
            raise

        print("7 - output file")

        output_file = self.converter.build_output_file(
            file_path,
            job,
            output_path,
        )

        if output_file.exists:
            self.logger.info(
                f"Output already exists: {output_file.output_path}"
            )

            checked = self._validate_output(media, output_file.output_path, job)
            if checked.is_valid:
                self.logger.info(
                    f"Output already valid: {output_file.output_path}"
                )

                return ProcessResult(
                    success=True,
                    skipped=True,
                    input_path=file_path,
                    output_path=output_file.output_path,
                )

            self.logger.info(
                f"Output requires rebuild: {output_file.output_path} - "
                + "; ".join(checked.errors)
            )

        self.logger.info(f"Conversion started: {file_path.name}")

        monitor = ConversionMonitor(
            LOGS_DIR / "conversion"
        )
        print("8 - execute ffmpeg")
        return_code = self.converter.execute(
            file_path,
            job,
            output_file.output_path,
            monitor,
            on_progress,
        )

        if return_code == 0:

            validation = self._validate_output(
                media, output_file.output_path, job,
            )

            if not validation.is_valid:

                self.logger.error(
                    f"Output validation failed: {output_file.output_path.name} - "
                    + "; ".join(validation.errors)
                )

                monitor.append_log("")
                monitor.append_log("=" * 80)
                monitor.append_log("OUTPUT VALIDATION FAILED")
                monitor.append_log("=" * 80)

                for error in validation.errors:
                    monitor.append_log(f"- {error}")

                monitor.append_log("=" * 80)

                return ProcessResult(
                    success=False,
                    skipped=False,
                    input_path=file_path,
                    output_path=output_file.output_path,
                    error="\n".join(validation.errors),
                )

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
            f"Conversion failed: {file_path.name} "
            f"(return code: {return_code})"
        )

        return ProcessResult(
            success=False,
            skipped=False,
            input_path=file_path,
            output_path=output_file.output_path,
            error=f"Return code: {return_code}",
        )
