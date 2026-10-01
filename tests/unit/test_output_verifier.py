import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from core.models.subtitle_track import SubtitleTrack
from core.models.media_language import MediaLanguage
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

    def test_single_main_video_accepts_one_of_two_source_video_tracks(self):
        source = replace(self.source, video_tracks=[object(), object()])
        job = replace(self.job, single_main_video=True)
        self.assertTrue(self.verifier.verify(source, self.output, job).is_valid)
        missing = replace(self.output, video_tracks=[])
        self.assertFalse(self.verifier.verify(source, missing, job).is_valid)
        disabled = replace(job, include_video=False)
        self.assertTrue(self.verifier.verify(source, missing, disabled).is_valid)

    def subtitle(self, index, language, default=False, forced=False):
        return SubtitleTrack(index, "mov_text", MediaLanguage(language), "", default, forced)

    def check_subtitles(self, requested, actual, container="mp4"):
        job = replace(self.job, include_subtitles=True, subtitle_tracks=requested,
                      audio_tracks=[], include_audio=False, verify_composition=True)
        output = replace(self.output, container=container, audio_tracks=[], subtitle_tracks=actual)
        return self.verifier.verify(self.source, output, job).is_valid

    def test_mp4_single_forced_normalizes_default(self):
        track = self.subtitle(4, "spa", forced=True)
        self.assertTrue(self.check_subtitles([track], [replace(track, default=True)]))
        self.assertFalse(self.check_subtitles([track], [track]))

    def test_mp4_two_subtitles_normalize_only_first(self):
        for first_forced in (True, False):
            requested = [self.subtitle(4, "spa", forced=first_forced),
                         self.subtitle(5, "eng", forced=not first_forced)]
            actual = [replace(requested[0], default=True), requested[1]]
            self.assertTrue(self.check_subtitles(requested, actual))
            self.assertFalse(self.check_subtitles(requested, [actual[0], replace(actual[1], default=True)]))

    def test_explicit_default_remains_strict(self):
        requested = [self.subtitle(4, "spa", forced=True), self.subtitle(5, "eng", default=True)]
        self.assertTrue(self.check_subtitles(requested, requested))
        self.assertFalse(self.check_subtitles(requested, [replace(requested[0], default=True), replace(requested[1], default=False)]))
        self.assertFalse(self.check_subtitles(requested, [replace(requested[0], default=True), requested[1]]))

    def test_mp4_forced_and_composition_remain_strict(self):
        requested = [self.subtitle(4, "spa", forced=True), self.subtitle(5, "eng")]
        actual = [replace(requested[0], default=True), requested[1]]
        invalid = [[], actual[:1], actual + [self.subtitle(6, "jpn")],
                   list(reversed(actual)), [replace(actual[0], forced=False), actual[1]],
                   [replace(actual[0], codec="subrip"), actual[1]],
                   [replace(actual[0], language=MediaLanguage("jpn")), actual[1]]]
        for tracks in invalid:
            self.assertFalse(self.check_subtitles(requested, tracks))

    def test_other_container_preserves_requested_default(self):
        track = self.subtitle(4, "spa", forced=True)
        self.assertTrue(self.check_subtitles([track], [track], container="mkv"))
        self.assertFalse(self.check_subtitles([track], [replace(track, default=True)], container="mkv"))

    def test_copy_default_still_requires_all_source_video_tracks(self):
        source = replace(self.source, video_tracks=[object(), object()])
        self.assertFalse(self.job.single_main_video)
        result = self.verifier.verify(source, self.output, self.job)
        self.assertFalse(result.is_valid)
        self.assertIn("Missing video tracks: expected at least 2, found 1.", result.errors)
        complete = replace(self.output, video_tracks=list(source.video_tracks))
        self.assertTrue(self.verifier.verify(source, complete, self.job).is_valid)


if __name__ == "__main__":
    unittest.main()
