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

        # Match Converter's video policy, selected audio (or all),
        # and only explicitly selected subtitles. Output indices can change.
        expected_video = 0
        if job.include_video:
            expected_video = 1 if job.single_main_video else len(source.video_tracks)
        expected = (
            ("video", expected_video, len(output.video_tracks)),
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
        if job.verify_composition:
            for kind, count, actual in expected:
                if actual > count:
                    errors.append(f"Unexpected {kind} tracks: expected {count}, found {actual}.")
            audio = list(job.audio_tracks or source.audio_tracks) if job.include_audio else []
            if job.default_audio_track in audio:
                audio.remove(job.default_audio_track)
                audio.insert(0, job.default_audio_track)
            subtitles = list(job.subtitle_tracks or []) if job.include_subtitles else []
            # MOV/MP4 enables the first subtitle when none is explicitly default.
            mp4_subtitle_default = (
                output.container.lower() == "mp4"
                and bool(subtitles)
                and not any(track.default for track in subtitles)
            )
            for kind, selected, actual, codecs in (
                ("audio", audio, output.audio_tracks, job.audio_codecs),
                ("subtitle", subtitles, output.subtitle_tracks, job.subtitle_codecs),
            ):
                for index, (track, found) in enumerate(zip(selected, actual)):
                    codec = (codecs or {}).get(track.stream_index, "copy")
                    wanted_codec = track.codec if codec == "copy" else codec
                    wanted_default = (track is job.default_audio_track if kind == "audio" and codecs is not None else track.default)
                    if kind == "subtitle" and mp4_subtitle_default:
                        wanted_default = index == 0
                    signature = (wanted_codec.lower(), track.language.code or "und",
                                 wanted_default, track.forced)
                    observed = (found.codec.lower(), found.language.code or "und",
                                found.default, found.forced)
                    if signature != observed or (kind == "audio" and track.channels != found.channels):
                        errors.append(f"{kind.title()} composition mismatch at output stream {index}.")
        return ValidationResult(is_valid=not errors, errors=errors)
