from core.models.media_file import MediaFile

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

        result = ValidationResult(
            is_valid=True
        )

        self._validate_video_tracks(
            media,
            result,
        )

        self._validate_container(
            media,
            result,
        )

        result.is_valid = (
            len(result.errors) == 0
        )

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

    def _validate_container(
        self,
        media: MediaFile,
        result: ValidationResult,
    ) -> None:
        """
        Verifica que el contenedor sea MP4.
        """

        if media.container.lower() != "mov,mp4,m4a,3gp,3g2,mj2":
            result.errors.append(
                (
                    "Container must be MP4 "
                    f"(found '{media.container}')."
                )
            )