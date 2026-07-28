from core.models.media_file import MediaFile

from modules.planning.conversion_plan import (
    ConversionPlan,
)

from modules.validation.validation_result import (
    ValidationResult,
)


class ConversionPlanner:
    """
    Determines the minimum conversion required for
    a media file to satisfy the target profile.

    The planner decides WHAT should be done.

    It never decides HOW FFmpeg should perform it.
    """

    def plan(
        self,
        media: MediaFile,
        validation: ValidationResult,
    ) -> ConversionPlan:

        if validation.is_valid:
            return ConversionPlan(
                compatible=True,
                remux_container=False,
                convert_video=False,
                convert_audio=False,
                reason="Already compatible.",
            )

        #
        # Temporary implementation.
        # The planner currently interprets human-readable
        # validation messages.
        #
        # Future versions should consume structured
        # ValidationIssue objects instead.
        #

        errors = "\n".join(validation.errors)

        video_errors = (
            "Video codec",
            "Pixel format",
            "Video profile",
            "Video level",
        )

        audio_errors = ("Audio codec",)

        has_container_error = "Container" in errors

        has_video_error = any(text in errors for text in video_errors)

        has_audio_error = any(text in errors for text in audio_errors)

        #
        # Remux only
        #

        if has_container_error and not has_video_error and not has_audio_error:
            return ConversionPlan(
                compatible=False,
                remux_container=True,
                convert_video=False,
                convert_audio=False,
                reason="Container remux required.",
            )

        #
        # Video conversion
        #

        if has_video_error:
            return ConversionPlan(
                compatible=False,
                remux_container=False,
                convert_video=True,
                convert_audio=False,
                reason="Video conversion required.",
            )

        #
        # Audio conversion
        #

        if has_audio_error:
            return ConversionPlan(
                compatible=False,
                remux_container=False,
                convert_video=False,
                convert_audio=True,
                reason="Audio conversion required.",
            )

        #
        # Fallback
        #

        return ConversionPlan(
            compatible=False,
            remux_container=False,
            convert_video=False,
            convert_audio=False,
            reason="Manual review required.",
        )
