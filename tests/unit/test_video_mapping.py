import unittest
from pathlib import Path

from core.models.conversion_job import ConversionJob
from core.models.media_file import MediaFile
from modules.conversion.conversion_job_builder import ConversionJobBuilder
from modules.converter.converter import Converter
from modules.planning.conversion_plan import ConversionPlan


class VideoMappingTests(unittest.TestCase):
    def command(self, job):
        return Converter().build_command(Path("input.mkv"), job, Path("output.mp4"))

    def test_builder_selects_first_non_attached_video_for_encode_and_remux(self):
        media = MediaFile("mkv", 100.0, 1000, 0, [], [], [])
        for encode in (True, False):
            with self.subTest(encode=encode):
                plan = ConversionPlan(False, not encode, encode, False, "test")
                job = ConversionJobBuilder().build(media, plan)
                self.assertTrue(job.single_main_video)
                command = self.command(job)
                maps = [command[i + 1] for i, value in enumerate(command) if value == "-map"]
                self.assertIn("0:V:0", maps)
                self.assertNotIn("0:v", maps)
                self.assertEqual(command[command.index("-c:v") + 1], "libx264" if encode else "copy")

    def test_default_job_preserves_all_video_mapping(self):
        job = ConversionJob()
        self.assertFalse(job.single_main_video)
        command = self.command(job)
        self.assertEqual(command[command.index("-map") + 1], "0:v")

    def test_disabled_video_emits_no_video_mapping(self):
        job = ConversionJob(single_main_video=True, include_video=False, include_audio=False)
        command = self.command(job)
        self.assertNotIn("-map", command)
        self.assertNotIn("-c:v", command)


if __name__ == "__main__":
    unittest.main()
