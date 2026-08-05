from core.models.media_file import MediaFile

from core.models.conversion_job import (
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
        conversion_settings: dict | None = None,
    ) -> ConversionJob:
        """
        Build a WebSafe conversion job.

        The builder translates the planner decisions
        into concrete conversion targets understood
        by the Converter.
        """

        audio_languages: list[str] = []

        subtitle_languages: list[str] = []

        default_audio_language: str | None = None

        if conversion_settings is not None:

            audio_languages = (
                conversion_settings.get(
                    "audio",
                    [],
                )
            )

            subtitle_languages = (
                conversion_settings.get(
                    "subtitles",
                    [],
                )
            )

            default_audio_language = (
                conversion_settings.get(
                    "default_audio",
                )
            )

        return ConversionJob(
            # Container
            target_container="mp4",

            # Video
            convert_video=plan.convert_video,
            target_video_codec=(
                "libx264"
                if plan.convert_video
                else None
            ),
            target_profile=(
                "high"
                if plan.convert_video
                else None
            ),
            target_pixel_format=(
                "yuv420p"
                if plan.convert_video
                else None
            ),
            target_level=(
                4.1
                if plan.convert_video
                else None
            ),

            # Audio
            convert_audio=plan.convert_audio,
            target_audio_codec=(
                "aac"
                if plan.convert_audio
                else None
            ),

            # Streams
            include_video=True,
            include_audio=True,
            include_subtitles=False,

            # Language preferences
            audio_languages=audio_languages,
            subtitle_languages=subtitle_languages,
            default_audio_language=(
                default_audio_language
            ),
        )