from pathlib import Path
import subprocess

from core.constants.paths import OUTPUT_DIR
from core.models.conversion_job import ConversionJob
from core.models.output_file import OutputFile


class Converter:
    def build_command(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
    ) -> list[str]:
        if output_path is None:
            output_path = OUTPUT_DIR / f"{file_path.stem}.{job.target_container}"

        command = [
            "ffmpeg",
            "-i",
            str(file_path),
        ]

        if job.include_video:
            command.extend(
                [
                    "-map",
                    "0:v",
                ]
            )

            if job.convert_video:
                command.extend(
                    [
                        "-c:v",
                        job.target_video_codec,
                    ]
                )
            else:
                command.extend(
                    [
                        "-c:v",
                        "copy",
                    ]
                )

        if job.include_audio:
            command.extend(
                [
                    "-map",
                    "0:a",
                ]
            )

            if job.convert_audio:
                command.extend(
                    [
                        "-c:a",
                        job.target_audio_codec,
                    ]
                )
            else:
                command.extend(
                    [
                        "-c:a",
                        "copy",
                    ]
                )

        if job.include_subtitles:
            command.extend(
                [
                    "-map",
                    "0:s",
                ]
            )

            if job.convert_subtitles:
                command.extend(
                    [
                        "-c:s",
                        job.target_subtitle_codec,
                    ]
                )
            else:
                command.extend(
                    [
                        "-c:s",
                        "copy",
                    ]
                )

        command.append(str(output_path))

        return command

    def build_output_file(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
    ) -> OutputFile:
        if output_path is None:
            output_path = OUTPUT_DIR / f"{file_path.stem}.{job.target_container}"

        return OutputFile(
            source_path=file_path,
            output_path=output_path,
            container=job.target_container,
            exists=output_path.exists(),
        )

    def execute(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
    ) -> int:
        if output_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        command = self.build_command(
            file_path,
            job,
            output_path,
        )

        print()
        print("EXECUTING")
        print("----------")
        print(" ".join(command))
        print()

        result = subprocess.run(command)

        return result.returncode
