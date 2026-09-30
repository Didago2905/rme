import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from core.models.conversion_job import ConversionJob
from modules.converter.converter import Converter


class ConverterOverwriteTests(unittest.TestCase):
    def test_default_command_refuses_overwrite_without_interaction(self):
        command = Converter().build_command(
            Path("source.mkv"), ConversionJob(), Path("output.mp4"),
        )
        self.assertIn("-nostdin", command)
        self.assertIn("-n", command)
        self.assertNotIn("-y", command)

    def test_authorized_command_overwrites_without_interaction(self):
        command = Converter().build_command(
            Path("source.mkv"), ConversionJob(), Path("output.mp4"), overwrite=True,
        )
        self.assertIn("-nostdin", command)
        self.assertIn("-y", command)
        self.assertNotIn("-n", command)

    def test_execute_passes_policy_and_disconnects_stdin(self):
        with TemporaryDirectory() as directory:
            destination = Path(directory) / "output.mp4"
            for overwrite in (False, True):
                with self.subTest(overwrite=overwrite):
                    process = Mock(stderr=[])
                    process.wait.return_value = 0
                    with patch("modules.converter.converter.subprocess.Popen", return_value=process) as launch:
                        kwargs = {"overwrite": True} if overwrite else {}
                        result = Converter().execute(
                            Path("source.mkv"), ConversionJob(), destination, **kwargs,
                        )
                    self.assertEqual(result, 0)
                    self.assertEqual(launch.call_args.kwargs["stdin"], subprocess.DEVNULL)
                    command = launch.call_args.args[0]
                    self.assertIn("-nostdin", command)
                    self.assertIn("-y" if overwrite else "-n", command)
                    self.assertNotIn("-n" if overwrite else "-y", command)


if __name__ == "__main__":
    unittest.main()
