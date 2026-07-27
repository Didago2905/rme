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
    ) -> list[str]:

        output_file = OUTPUT_DIR / f"{file_path.stem}.{job.target_container}"

        command = [
            "ffmpeg",
            "-i",
            str(file_path),
        ]

        command.extend(
            [
                "-map",
                "0",
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

        command.append(str(output_file))

        return command

    def build_output_file(
        self,
        file_path: Path,
        job: ConversionJob,
    ) -> OutputFile:

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
    ) -> int:

        command = self.build_command(
            file_path,
            job,
        )

        print()
        print("EXECUTING")
        print("----------")
        print(" ".join(command))
        print()

        result = subprocess.run(command)

        return result.returncode
