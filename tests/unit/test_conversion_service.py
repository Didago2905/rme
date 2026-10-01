import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import Mock, patch

from core.models.conversion_job import ConversionJob
from core.models.media_item import MediaItem
from core.models.output_file import OutputFile
from modules.validation.output_verifier import OutputVerifier
from modules.validation.validation_result import ValidationResult
from services.conversion_service import ConversionService


class ConversionServiceTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.source_path = Path(self.directory.name) / "source.mkv"
        self.output_path = Path(self.directory.name) / "output.mp4"
        self.source_path.write_bytes(b"source")
        self.source = MediaItem("source.mkv", self.source_path, "mkv", 5520, 6, 0,
                                [object()], [object()], [object()])
        self.output = MediaItem("output.mp4", self.output_path, "mp4", 5520, 6, 0,
                                [object()], [object()], [object()])
        audio = SimpleNamespace(stream_index=1, codec="aac", language=SimpleNamespace(code="eng"),
                                title="", default=False, forced=False, channels=2)
        subtitle = SimpleNamespace(stream_index=2, codec="mov_text", language=SimpleNamespace(code="eng"),
                                   title="", default=True, forced=False)
        self.source.audio_tracks = [audio]
        self.output.audio_tracks = [audio]
        self.source.subtitle_tracks = [subtitle]
        self.output.subtitle_tracks = [subtitle]
        self.service = ConversionService.__new__(ConversionService)
        self.service.media_service = Mock()
        self.service.media_service.get_media.side_effect = lambda path: self.source if path == self.source_path else self.output
        self.service.validation_service = Mock()
        self.service.validation_service.validate.return_value = ValidationResult(True)
        self.service.output_verifier = OutputVerifier()
        self.service.conversion_planner = Mock()
        self.service.conversion_planner.plan.return_value = SimpleNamespace(compatible=False)
        self.service.conversion_job_builder = Mock()
        self.service.conversion_job_builder.build.return_value = ConversionJob()
        self.service.converter = Mock()
        self.service.converter.cancelled = False
        self.service.converter.build_output_file.side_effect = lambda *args: OutputFile(self.source_path, self.output_path, "mp4", self.output_path.exists())
        self.service.converter.execute.side_effect = self.execute
        self.service.logger = Mock()
        self.monitor = Mock()
        patcher = patch("services.conversion_service.ConversionMonitor", return_value=self.monitor)
        patcher.start()
        self.addCleanup(patcher.stop)

    def execute(self, *args, **kwargs):
        self.output_path.write_bytes(b"output")
        return 0

    def run_conversion(self):
        return self.service.process_file(self.source_path, self.output_path)

    def test_ffmpeg_success(self):
        result = self.run_conversion()
        self.assertTrue(result.success)
        self.assertFalse(result.skipped)
        self.assertEqual(self.service.validation_service.validate.call_count, 2)
        self.assertIs(self.service.converter.execute.call_args.kwargs["overwrite"], False)

    def test_default_encoder_forwarded(self):
        self.run_conversion()
        self.assertEqual(self.service.conversion_job_builder.build.call_args.kwargs,
                         {"video_encoder": "libx264"})

    def test_explicit_nvenc_forwarded_with_track_settings(self):
        settings = {"video_encoder": "h264_nvenc", "audio_tracks": self.source.audio_tracks,
                    "subtitle_tracks": self.source.subtitle_tracks}
        self.service.process_file(self.source_path, self.output_path, settings)
        args = self.service.conversion_job_builder.build.call_args
        self.assertIs(args.args[2], settings)
        self.assertEqual(args.kwargs, {"video_encoder": "h264_nvenc"})

    def test_zero_exit_truncation_fails_before_websafe(self):
        self.output.duration_seconds = 840
        result = self.run_conversion()
        self.assertFalse(result.success)
        self.assertIn("Duration mismatch", result.error)
        self.assertEqual(self.service.validation_service.validate.call_count, 1)
        self.assertTrue(any("840" in str(call) for call in self.monitor.append_log.call_args_list))

    def test_nonzero_exit(self):
        self.service.converter.execute.side_effect = None
        self.service.converter.execute.return_value = 1
        result = self.run_conversion()
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Return code: 1")

    def test_missing_empty_unreadable_output(self):
        for mode in ["missing", "empty", "unreadable"]:
            with self.subTest(mode=mode):
                self.output_path.unlink(missing_ok=True)
                self.service.converter.execute.side_effect = lambda *args, **kwargs: 0
                if mode != "missing":
                    self.output_path.write_bytes(b"data" if mode == "unreadable" else b"")
                if mode == "unreadable":
                    self.service.media_service.get_media.side_effect = lambda path: self.source if path == self.source_path else (_ for _ in ()).throw(ValueError("probe failed"))
                self.assertFalse(self.run_conversion().success)

    def test_websafe_still_required(self):
        self.service.validation_service.validate.side_effect = [ValidationResult(True), ValidationResult(False, ["Video codec"])]
        result = self.run_conversion()
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Video codec")

    def test_existing_valid_is_skipped(self):
        self.output_path.write_bytes(b"output")
        result = self.run_conversion()
        self.assertTrue(result.success and result.skipped)
        self.service.converter.execute.assert_not_called()
        self.assertEqual(self.output_path.read_bytes(), b"output")

    def test_existing_truncated_rebuild_must_pass(self):
        self.output_path.write_bytes(b"output")
        self.output.duration_seconds = 840
        self.assertFalse(self.run_conversion().success)
        self.service.converter.execute.assert_called_once()
        self.assertIs(self.service.converter.execute.call_args.kwargs["overwrite"], True)

    def test_existing_truncated_rebuild_can_succeed(self):
        self.output_path.write_bytes(b"output")
        self.output.duration_seconds = 840
        def rebuild(*args, **kwargs):
            self.assertEqual(self.output_path.read_bytes(), b"output")
            self.assertIs(kwargs["overwrite"], True)
            self.output.duration_seconds = 5520
            return self.execute(*args, **kwargs)
        self.service.converter.execute.side_effect = rebuild
        result = self.run_conversion()
        self.assertTrue(result.success)
        self.assertFalse(result.skipped)

    def test_copy_is_verified(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        result = self.run_conversion()
        self.assertTrue(result.success and result.skipped)
        self.assertEqual(self.output_path.read_bytes(), b"source")
        self.service.converter.execute.assert_not_called()

    def test_copy_truncated_or_missing_tracks_fails(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        self.output.duration_seconds = 840
        self.assertFalse(self.run_conversion().success)
        self.output.duration_seconds = 5520
        self.output.subtitle_tracks = []
        self.assertFalse(self.run_conversion().success)

    def test_existing_copy_is_checked_and_replaced(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        self.output_path.write_bytes(b"truncated")
        self.output.duration_seconds = 840
        with patch("services.conversion_service.copy2") as copy:
            def replace_copy(*args):
                self.output.duration_seconds = 5520
            copy.side_effect = replace_copy
            result = self.run_conversion()
        self.assertTrue(result.success and result.skipped)
        copy.assert_called_once()

    def test_existing_copy_valid_is_not_rewritten(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        self.output_path.write_bytes(b"output")
        with patch("services.conversion_service.copy2") as copy:
            result = self.run_conversion()
        self.assertTrue(result.success and result.skipped)
        copy.assert_not_called()

    def test_copy_error_or_empty_copy_is_failed(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        with patch("services.conversion_service.copy2", side_effect=OSError("copy failed")):
            self.assertFalse(self.run_conversion().success)
        with patch("services.conversion_service.copy2", side_effect=lambda *args: self.output_path.touch()):
            self.assertFalse(self.run_conversion().success)

    def test_ffmpeg_missing_selected_tracks_fails_before_websafe(self):
        self.service.conversion_job_builder.build.return_value = ConversionJob(
            include_subtitles=True, subtitle_tracks=self.source.subtitle_tracks,
        )
        self.output.subtitle_tracks = []
        result = self.run_conversion()
        self.assertFalse(result.success)
        self.assertIn("Missing subtitle tracks", result.error)
        self.assertEqual(self.service.validation_service.validate.call_count, 1)

    def test_copy_still_requires_websafe(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        self.service.validation_service.validate.side_effect = [
            ValidationResult(True), ValidationResult(False, ["Video codec"]),
        ]
        self.assertFalse(self.run_conversion().success)

    def test_compatible_source_without_destination_is_verified(self):
        self.service.conversion_planner.plan.return_value.compatible = True
        self.source.duration_seconds = float("nan")
        result = self.service.process_file(self.source_path)
        self.assertFalse(result.success)
        self.assertFalse(result.skipped)

    def test_cancelled_before_analysis_does_not_launch(self):
        self.service.converter.cancelled = True
        result = self.run_conversion()
        self.assertTrue(result.cancelled)
        self.assertFalse(result.success)
        self.service.media_service.get_media.assert_not_called()
        self.service.converter.execute.assert_not_called()

    def test_cancelled_after_probe_does_not_launch(self):
        def probe(path):
            self.service.converter.cancelled = True
            return self.source
        self.service.media_service.get_media.side_effect = probe
        self.assertTrue(self.run_conversion().cancelled)
        self.service.converter.execute.assert_not_called()

    def test_cancelled_ffmpeg_keeps_partial_output(self):
        def cancel(*args, **kwargs):
            self.output_path.write_bytes(b"partial")
            self.service.converter.cancelled = True
            return -1
        self.service.converter.execute.side_effect = cancel
        result = self.run_conversion()
        self.assertTrue(result.cancelled)
        self.assertFalse(result.success or result.skipped)
        self.assertEqual(self.output_path.read_bytes(), b"partial")
        self.assertEqual(self.service.validation_service.validate.call_count, 1)


if __name__ == "__main__":
    unittest.main()
