from math import isfinite

from core.models.conversion_job import ConversionJob
from core.models.media_item import MediaItem
from modules.validation.validation_result import ValidationResult


class OutputVerifier:
    """Verify completeness against the source and the requested stream mapping."""

    def verify(
        self, source: MediaItem, output: MediaItem, job: ConversionJob,
    ) -> ValidationResult:
        errors = []
        if not output.path.is_file() or output.path.stat().st_size == 0:
            errors.append("Output file is missing or empty.")

        durations = (source.duration_seconds, output.duration_seconds)
        if not all(isfinite(value) and value > 0 for value in durations):
            errors.append(
                f"Invalid duration: input={durations[0]}s, output={durations[1]}s."
            )
        else:
            tolerance = max(2.0, source.duration_seconds * 0.01)
            if abs(source.duration_seconds - output.duration_seconds) > tolerance:
                errors.append(
                    f"Duration mismatch: input={durations[0]}s, "
                    f"output={durations[1]}s, tolerance={tolerance}s."
                )

        # Match Converter's mapping: all video, selected audio (or all),
        # and only explicitly selected subtitles. Output indices can change.
        expected = (
            ("video", len(source.video_tracks) if job.include_video else 0,
             len(output.video_tracks)),
            ("audio", len(job.audio_tracks or source.audio_tracks)
             if job.include_audio else 0, len(output.audio_tracks)),
            ("subtitle", len(job.subtitle_tracks or [])
             if job.include_subtitles else 0, len(output.subtitle_tracks)),
        )
        for kind, count, actual in expected:
            if actual < count:
                errors.append(
                    f"Missing {kind} tracks: expected at least {count}, found {actual}."
                )
        return ValidationResult(is_valid=not errors, errors=errors)
