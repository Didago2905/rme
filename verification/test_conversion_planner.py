from modules.planning.conversion_planner import ConversionPlanner
from modules.validation.validation_result import ValidationResult


planner = ConversionPlanner()


def print_plan(title: str, validation: ValidationResult):

    plan = planner.plan(
        media=None,
        validation=validation,
    )

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    print(f"Compatible      : {plan.compatible}")
    print(f"Remux Container : {plan.remux_container}")
    print(f"Convert Video   : {plan.convert_video}")
    print(f"Convert Audio   : {plan.convert_audio}")
    print(f"Reason          : {plan.reason}")


#
# Compatible
#

print_plan(
    "COMPATIBLE FILE",
    ValidationResult(
        is_valid=True,
        errors=[],
        warnings=[],
    ),
)


#
# Remux
#

print_plan(
    "REMUX ONLY",
    ValidationResult(
        is_valid=False,
        errors=[
            "Container must be MP4.",
        ],
        warnings=[],
    ),
)


#
# Video conversion
#

print_plan(
    "VIDEO CONVERSION",
    ValidationResult(
        is_valid=False,
        errors=[
            "Video codec must be H264.",
        ],
        warnings=[],
    ),
)


#
# Audio conversion
#

print_plan(
    "AUDIO CONVERSION",
    ValidationResult(
        is_valid=False,
        errors=[
            "Audio codec must be AAC.",
        ],
        warnings=[],
    ),
)