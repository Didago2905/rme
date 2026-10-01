import unittest
from dataclasses import replace
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

    def encoder_job(self, encoder, convert_video=True):
        media = MediaFile("mkv", 100.0, 1000, 0, [], [], [])
        plan = ConversionPlan(False, not convert_video, convert_video, False, "test")
        job = ConversionJobBuilder().build(media, plan, video_encoder=encoder)
        return replace(job, include_audio=False)

    def test_nvenc_v1_exact_video_arguments(self):
        command = self.command(self.encoder_job("h264_nvenc"))
        self.assertEqual(command[command.index("-c:v"):-1], [
            "-c:v", "h264_nvenc", "-preset", "p4", "-tune", "hq",
            "-rc", "vbr", "-cq", "23", "-b:v", "0",
            "-multipass", "disabled", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-level:v", "4.1",
        ])

    def test_libx264_video_arguments_unchanged(self):
        command = self.command(self.encoder_job("libx264"))
        self.assertEqual(command[command.index("-c:v"):-1], [
            "-c:v", "libx264", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-level:v", "4.1",
        ])

    def test_copy_ignores_encoder_options(self):
        job = self.encoder_job("h264_nvenc", convert_video=False)
        self.assertEqual(job.video_encoder_options, ())
        # Even a manually populated job must not apply encoder options to COPY.
        job = replace(job, video_encoder_options=("-preset", "p4"))
        command = self.command(job)
        self.assertEqual(command[command.index("-c:v"):-1], ["-c:v", "copy"])

    def test_unsupported_transcode_encoder_rejected(self):
        with self.assertRaises(ValueError):
            self.encoder_job("unknown")

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
