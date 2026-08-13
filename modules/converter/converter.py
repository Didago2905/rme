from collections.abc import Callable
from pathlib import Path
import subprocess

from core.constants.paths import OUTPUT_DIR
from core.models.conversion_job import ConversionJob
from core.models.ffmpeg_progress import FFmpegProgress
from core.models.output_file import OutputFile
from modules.conversion.conversion_monitor import ConversionMonitor
from modules.converter.ffmpeg_progress_parser import FFmpegProgressParser


class Converter:

    def build_command(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
    ) -> list[str]:

        try:

            if output_path is None:
                output_path = (
                    OUTPUT_DIR
                    / f"{file_path.stem}.{job.target_container}"
                )

            command = [
                "ffmpeg",
                "-progress",
                "pipe:2",
                "-nostats",
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

                    if job.target_profile is not None:

                        command.extend(
                            [
                                "-profile:v",
                                job.target_profile,
                            ]
                        )

                    if job.target_pixel_format is not None:

                        command.extend(
                            [
                                "-pix_fmt",
                                job.target_pixel_format,
                            ]
                        )

                    if job.target_level is not None:

                        command.extend(
                            [
                                "-level:v",
                                str(job.target_level),
                            ]
                        )

                else:

                    command.extend(
                        [
                            "-c:v",
                            "copy",
                        ]
                    )

            command.extend(
                self._build_audio_command(job)
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

            command.append(
                str(output_path)
            )

            return command

        except Exception as error:

            print(
                "ERROR build_command:",
                repr(error),
            )

            raise

    def _build_audio_command(
        self,
        job: ConversionJob,
    ) -> list[str]:

        command = []

        if not job.include_audio:
            return command

        audio_tracks = list(
            job.audio_tracks or []
        )

        if not audio_tracks:

            command.extend(
                [
                    "-map",
                    "0:a",
                ]
            )

        else:

            default_track = (
                job.default_audio_track
            )

            if (
                default_track is not None
                and default_track in audio_tracks
            ):

                audio_tracks.remove(
                    default_track
                )

                audio_tracks.insert(
                    0,
                    default_track
                )

            for track in audio_tracks:

                command.extend(
                    [
                        "-map",
                        f"0:{track.stream_index}",
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

        if audio_tracks:

            for index, track in enumerate(
                audio_tracks
            ):

                if (
                    job.default_audio_track
                    is not None
                    and track
                    is job.default_audio_track
                ):

                    command.extend(
                        [
                            f"-disposition:a:{index}",
                            "default",
                        ]
                    )

                else:

                    command.extend(
                        [
                            f"-disposition:a:{index}",
                            "0",
                        ]
                    )

        return command

    def build_output_file(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
    ) -> OutputFile:

        if output_path is None:
            output_path = (
                OUTPUT_DIR
                / f"{file_path.stem}.{job.target_container}"
            )

        return OutputFile(
            source_path=file_path,
            output_path=output_path,
            container=job.target_container,
            exists=output_path.exists(),
        )

    def _subprocess_kwargs(
        self,
    ) -> dict:

        if subprocess.os.name != "nt":
            return {}

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= (
            subprocess.STARTF_USESHOWWINDOW
        )

        return {
            "startupinfo": startupinfo,
            "creationflags": (
                subprocess.CREATE_NO_WINDOW
            ),
        }

    def execute(
        self,
        file_path: Path,
        job: ConversionJob,
        output_path: Path | None = None,
        monitor: ConversionMonitor | None = None,
        on_progress: (
            Callable[
                [FFmpegProgress],
                None,
            ]
            | None
        ) = None,
    ) -> int:

        print("9 - inside converter.execute")

        if output_path is not None:

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        command = self.build_command(
            file_path,
            job,
            output_path,
        )

        if monitor is not None:

            monitor.append_log("=" * 80)
            monitor.append_log(
                "Starting FFmpeg conversion"
            )
            monitor.append_log("")
            monitor.append_log("Command:")
            monitor.append_log(
                " ".join(command)
            )
            monitor.append_log("")
            monitor.append_log("-" * 80)
            monitor.append_log(
                "FFmpeg Output"
            )
            monitor.append_log("-" * 80)
            monitor.append_log("")
            monitor.append_log("[STDERR]")

        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            **self._subprocess_kwargs(),
        )

        print("10 - ffmpeg launched")

        parser = FFmpegProgressParser()

        if process.stderr is not None:

            for line in process.stderr:

                line = line.strip()

                if not line:
                    continue

                if monitor is not None:
                    monitor.append_log(line)

                progress = parser.parse(line)

                if (
                    progress is not None
                    and on_progress is not None
                ):
                    on_progress(progress)

        return_code = process.wait()

        print(
            f"11 - return code = {return_code}"
        )

        if monitor is not None:

            monitor.append_log("")
            monitor.append_log("-" * 80)
            monitor.append_log(
                f"Exit code: {return_code}"
            )
            monitor.append_log("=" * 80)

        return return_code