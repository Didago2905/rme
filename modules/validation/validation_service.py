from core.models.media_file import MediaFile
from core.specifications.websafe import WEBSAFE_SPEC

from modules.validation.validation_result import (
    ValidationResult,
)


class ValidationService:
    """
    Evalúa un MediaFile contra la especificación
    WebSafe de RME.
    """

    def validate(
        self,
        media: MediaFile,
    ) -> ValidationResult:
        """
        Valida un archivo multimedia contra la
        especificación WebSafe.
        """

        result = ValidationResult(is_valid=True)

        self._validate_video_tracks(
            media,
            result,
        )

        self._validate_audio_tracks(
            media,
            result,
        )

        self._validate_container(
            media,
            result,
        )

        self._validate_video_codec(
            media,
            result,
        )

        self._validate_pixel_format(
            media,
            result,
        )

        self._validate_profile(
            media,
            result,
        )

        self._validate_level(
            media,
            result,
        )

        self._validate_audio_codec(
            media,
            result,
        )

        result.is_valid = len(result.errors) == 0

        return result

    def _validate_video_tracks(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que exista al menos una pista de video.
        """

        if len(media.video_tracks) == 0:
            result.errors.append(
                "The media file does not contain a video track."
            )

    def _validate_audio_tracks(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que exista al menos una pista de audio.
        """

        if len(media.audio_tracks) == 0:
            result.errors.append(
                "The media file does not contain an audio track."
            )

    def _validate_container(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el contenedor cumpla con la
        especificación WebSafe.
        """

        if media.container.lower() != WEBSAFE_SPEC["container"]:
            result.errors.append(
                (
                    "Container must be MP4 "
                    f"(found '{media.container}')."
                )
            )

    def _validate_video_codec(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el códec de video cumpla con la
        especificación WebSafe.
        """

        if len(media.video_tracks) == 0:
            return

        video = media.video_tracks[0]

        if (
            video.codec.lower()
            != WEBSAFE_SPEC["video_codec"]
        ):
            result.errors.append(
                (
                    "Video codec must be "
                    f"{WEBSAFE_SPEC['video_codec'].upper()} "
                    f"(found '{video.codec}')."
                )
            )

    def _validate_pixel_format(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el formato de píxel cumpla con la
        especificación WebSafe.
        """

        if len(media.video_tracks) == 0:
            return

        video = media.video_tracks[0]

        if (
            video.pixel_format
            not in WEBSAFE_SPEC["pixel_formats"]
        ):
            result.errors.append(
                (
                    "Pixel format must be "
                    f"{', '.join(WEBSAFE_SPEC['pixel_formats'])} "
                    f"(found '{video.pixel_format}')."
                )
            )

    def _validate_profile(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el perfil de video cumpla con la
        especificación WebSafe.
        """

        if len(media.video_tracks) == 0:
            return

        video = media.video_tracks[0]

        if (
            video.profile
            not in WEBSAFE_SPEC["profiles"]
        ):
            result.errors.append(
                (
                    "Video profile must be "
                    f"{', '.join(WEBSAFE_SPEC['profiles'])} "
                    f"(found '{video.profile}')."
                )
            )

    def _validate_level(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el nivel de video cumpla con la
        especificación WebSafe.
        """

        if len(media.video_tracks) == 0:
            return

        video = media.video_tracks[0]

        if video.level is None:
            return

        if video.level > WEBSAFE_SPEC["max_level"]:
            result.errors.append(
                (
                    "Video level must be "
                    f"{WEBSAFE_SPEC['max_level']:.1f} "
                    f"or lower (found {video.level:.1f})."
                )
            )

    def _validate_audio_codec(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el códec de audio cumpla con la
        especificación WebSafe.
        """

        if len(media.audio_tracks) == 0:
            return

        audio = media.audio_tracks[0]

        if (
            audio.codec.lower()
            not in WEBSAFE_SPEC["audio_codecs"]
        ):
            result.errors.append(
                (
                    "Audio codec must be "
                    f"{', '.join(codec.upper() for codec in WEBSAFE_SPEC['audio_codecs'])} "
                    f"(found '{audio.codec}')."
                )
            )