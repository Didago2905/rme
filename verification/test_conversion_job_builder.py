from modules.conversion.conversion_job_builder import (
    ConversionJobBuilder,
)

from modules.planning.conversion_plan import (
    ConversionPlan,
)


builder = ConversionJobBuilder()


def print_job(title: str, plan: ConversionPlan):

    job = builder.build(
        media=None,
        plan=plan,
    )

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    print(f"Target Container : {job.target_container}")
    print(f"Convert Video   : {job.convert_video}")
    print(f"Video Codec     : {job.target_video_codec}")
    print(f"Convert Audio   : {job.convert_audio}")
    print(f"Audio Codec     : {job.target_audio_codec}")


#
# Already compatible
#

print_job(
    "COMPATIBLE FILE",
    ConversionPlan(
        compatible=True,
        remux_container=False,
        convert_video=False,
        convert_audio=False,
        reason="Already compatible.",
    ),
)


#
# Remux only
#

print_job(
    "REMUX ONLY",
    ConversionPlan(
        compatible=False,
        remux_container=True,
        convert_video=False,
        convert_audio=False,
        reason="Container remux required.",
    ),
)


#
# Video conversion
#

print_job(
    "VIDEO CONVERSION",
    ConversionPlan(
        compatible=False,
        remux_container=False,
        convert_video=True,
        convert_audio=False,
        reason="Video conversion required.",
    ),
)


#
# Audio conversion
#

print_job(
    "AUDIO CONVERSION",
    ConversionPlan(
        compatible=False,
        remux_container=False,
        convert_video=False,
        convert_audio=True,
        reason="Audio conversion required.",
    ),
)