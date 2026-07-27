from core.models.compatibility_report import CompatibilityReport
from core.models.media_file import MediaFile


class Validator:
    def validate(
        self,
        media_file: MediaFile,
    ) -> CompatibilityReport:

        issues: list[str] = []

        container_ok = True
        video_ok = True
        audio_ok = True
        subtitle_ok = True

        if media_file.container != "mp4":
            container_ok = False

            issues.append(
                f"Unsupported container: {media_file.container}"
            )

        for video in media_file.video_tracks:
            if video.codec != "h264":
                video_ok = False

                issues.append(
                    f"Unsupported video codec: {video.codec}"
                )

        for audio in media_file.audio_tracks:
            if audio.codec != "aac":
                audio_ok = False

                issues.append(
                    f"Unsupported audio codec: {audio.codec}"
                )

        return CompatibilityReport(
            is_compatible=(
                container_ok
                and video_ok
                and audio_ok
                and subtitle_ok
            ),
            profile_name="web_safe",
            score=100 if not issues else 0,
            issues=issues,
            container_compatible=container_ok,
            video_compatible=video_ok,
            audio_compatible=audio_ok,
            subtitle_compatible=subtitle_ok,
        )