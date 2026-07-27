from core.models.media_file import MediaFile

from modules.validation.validation_result import (
    ValidationResult,
)
from modules.validation.validation_service import (
    ValidationService,
)


class ValidateMediaUseCase:
    """
    Caso de uso encargado de validar un MediaFile
    contra la especificación WebSafe.
    """

    def __init__(self) -> None:
        self._validation_service = (
            ValidationService()
        )

    def execute(
        self,
        media: MediaFile,
    ) -> ValidationResult:
        return self._validation_service.validate(
            media
        )