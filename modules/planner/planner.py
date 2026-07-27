from core.models.compatibility_report import CompatibilityReport
from core.models.conversion_job import ConversionJob


class Planner:
    def create_plan(
        self,
        report: CompatibilityReport,
    ) -> ConversionJob:

        job = ConversionJob(
            target_container="mp4",
            target_video_codec="h264",
            target_audio_codec="aac",
            target_subtitle_codec="mov_text",
        )

        if not report.container_compatible:
            job.remux_container = True

        if not report.video_compatible:
            job.convert_video = True

        if not report.audio_compatible:
            job.convert_audio = True

        if not report.subtitle_compatible:
            job.convert_subtitles = True

        return job