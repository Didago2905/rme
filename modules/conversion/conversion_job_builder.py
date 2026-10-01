from core.models.media_file import MediaFile
from core.specifications.websafe import WEBSAFE_SPEC
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
        *,
        video_encoder: str = "libx264",
    ) -> ConversionJob:
        """
        Build a WebSafe conversion job.

        The builder translates the planner decisions
        into concrete conversion targets understood
        by the Converter.
        """

        video_encoder_options = ()
        if plan.convert_video:
            if video_encoder not in ("libx264", "h264_nvenc"):
                raise ValueError(f"Unsupported video encoder: {video_encoder}")
            if video_encoder == "h264_nvenc":
                video_encoder_options = (
                    "-preset", "p4", "-tune", "hq", "-rc", "vbr",
                    "-cq", "23", "-b:v", "0", "-multipass", "disabled",
                )

        audio_tracks = []

        subtitle_tracks = []

        default_audio_track = None

        if conversion_settings is not None:

            audio_tracks = (
                conversion_settings.get(
                    "audio_tracks",
                    [],
                )
            )

            subtitle_tracks = (
                conversion_settings.get(
                    "subtitle_tracks",
                    [],
                )
            )

            default_audio_track = (
                conversion_settings.get(
                    "default_audio_track",
                )
            )

        # Empty audio selection retains the existing all-audio semantics.
        audio_tracks = list(audio_tracks or media.audio_tracks)
        if default_audio_track is not None and default_audio_track not in audio_tracks:
            default_audio_track = audio_tracks[0] if audio_tracks else None
        if default_audio_track is not None and default_audio_track in audio_tracks:
            audio_tracks.remove(default_audio_track)
            audio_tracks.insert(0, default_audio_track)
        audio_codecs = {
            track.stream_index: ("copy" if track.codec.lower() in WEBSAFE_SPEC["audio_codecs"] else "aac")
            for track in audio_tracks
        }
        subtitle_codecs = {
            track.stream_index: ("copy" if track.codec.lower() == "mov_text" else "mov_text")
            for track in subtitle_tracks
        }

        return ConversionJob(
            audio_codecs=audio_codecs,
            subtitle_codecs=subtitle_codecs,
            verify_composition=True,
            # Container
            target_container="mp4",

            # Video
            video_encoder_options=video_encoder_options,
            convert_video=plan.convert_video,
            target_video_codec=(
                video_encoder
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
            single_main_video=True,
            include_audio=True,
            include_subtitles=bool(
                subtitle_tracks
            ),

            # Selected tracks
            audio_tracks=audio_tracks,
            subtitle_tracks=subtitle_tracks,
            default_audio_track=(
                default_audio_track
            ),
        )
