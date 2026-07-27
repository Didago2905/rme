from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationResult:
    """
    Resultado de la validación de un archivo multimedia
    contra la especificación WebSafe.
    """

    is_valid: bool

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )