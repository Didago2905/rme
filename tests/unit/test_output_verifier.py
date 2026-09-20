import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from core.models.conversion_job import ConversionJob
from core.models.media_item import MediaItem
from modules.validation.output_verifier import OutputVerifier


def media(path, duration=100.0):
    return MediaItem(path.name, path, "mp4", duration, 4, 0,
                     [object()], [object(), object()], [object()])


class OutputVerifierTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "output.mp4"
        self.path.write_bytes(b"data")
        self.source = media(self.path)
        self.output = media(self.path)
        self.job = ConversionJob()
        self.verifier = OutputVerifier()

    def test_duration_boundaries(self):
        for source, output, valid in [(100, 98, True), (100, 102, True),
                                      (100, 97.99, False), (100, 102.01, False),
                                      (1000, 990, True), (1000, 989.99, False),
                                      (5520, 840, False)]:
            with self.subTest(source=source, output=output):
                result = self.verifier.verify(replace(self.source, duration_seconds=source),
                                              replace(self.output, duration_seconds=output), self.job)
                self.assertEqual(result.is_valid, valid)
                if source == 5520:
                    self.assertIn("input=5520s, output=840s", result.errors[0])

    def test_invalid_durations(self):
        for duration in [0, -1, float("nan"), float("inf"), -float("inf")]:
            for side in ["input", "output"]:
                with self.subTest(duration=duration, side=side):
                    source = replace(self.source, duration_seconds=duration) if side == "input" else self.source
                    output = replace(self.output, duration_seconds=duration) if side == "output" else self.output
                    self.assertFalse(self.verifier.verify(source, output, self.job).is_valid)

    def test_missing_empty_and_directory(self):
        self.path.unlink()
        self.assertFalse(self.verifier.verify(self.source, self.output, self.job).is_valid)
        self.path.touch()
        self.assertFalse(self.verifier.verify(self.source, self.output, self.job).is_valid)
        self.path.unlink()
        self.path.mkdir()
        self.assertFalse(self.verifier.verify(self.source, self.output, self.job).is_valid)

    def test_expected_mapping(self):
        selected = replace(self.job, audio_tracks=self.source.audio_tracks[:1],
                           include_subtitles=True, subtitle_tracks=self.source.subtitle_tracks)
        output = replace(self.output, audio_tracks=self.output.audio_tracks[:1])
        self.assertTrue(self.verifier.verify(self.source, output, selected).is_valid)
        self.assertFalse(self.verifier.verify(self.source, output, self.job).is_valid)
        for field in ["video_tracks", "audio_tracks", "subtitle_tracks"]:
            with self.subTest(field=field):
                self.assertFalse(self.verifier.verify(self.source, replace(output, **{field: []}), selected).is_valid)
        disabled = ConversionJob(include_video=False, include_audio=False, include_subtitles=False)
        self.assertTrue(self.verifier.verify(self.source, replace(output, video_tracks=[], audio_tracks=[], subtitle_tracks=[]), disabled).is_valid)

    def test_unselected_subtitles_are_not_required(self):
        output = replace(self.output, subtitle_tracks=[])
        self.assertTrue(self.verifier.verify(self.source, output, self.job).is_valid)


if __name__ == "__main__":
    unittest.main()
