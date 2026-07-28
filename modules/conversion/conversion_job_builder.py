from core.models.media_file import MediaFile

from modules.conversion.conversion_job import (
    ConversionJob,
)

from modules.planning.conversion_plan import (
    ConversionPlan,
)


class ConversionJobBuilder:
    """
    Builds a ConversionJob from a media file
    and a conversion plan.

    The builder translates high-level planning
    decisions into concrete conversion parameters.
    """

    def build(
        self,
        media: MediaFile,
        plan: ConversionPlan,
    ) -> ConversionJob:
        """
        Build a WebSafe conversion job.

        The builder translates the planner decisions
        into concrete conversion targets understood
        by the Converter.
        """

        return ConversionJob(
            target_container="mp4",

            convert_video=plan.convert_video,

            target_video_codec=(
                "h264"
                if plan.convert_video
                else None
            ),

            convert_audio=plan.convert_audio,

            target_audio_codec=(
                "aac"
                if plan.convert_audio
                else None
            ),
        )