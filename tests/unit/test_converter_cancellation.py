import io
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from core.models.conversion_job import ConversionJob
from modules.converter.converter import Converter


class FakeProcess:
    def __init__(self):
        self.stderr = io.StringIO()
        self.returncode = None
        self.terminations = 0

    def poll(self):
        return self.returncode

    def terminate(self):
        self.terminations += 1
        self.returncode = -1

    def wait(self, timeout=None):
        if self.returncode is None:
            self.returncode = 0
        return self.returncode


class ConverterCancellationTests(unittest.TestCase):
    def run_converter(self, converter):
        return converter.execute(Path("input.mkv"), ConversionJob())

    def test_cancel_only_owned_process_and_repeated_request(self):
        converter = Converter()
        own = FakeProcess()
        unrelated = FakeProcess()
        converter._process = own
        converter.cancel_current()
        converter.cancel_current()
        self.assertEqual(own.terminations, 1)
        self.assertEqual(unrelated.terminations, 0)

    def test_cancel_before_launch_and_prepare_next_job(self):
        converter = Converter()
        converter.cancel_current()
        with patch("modules.converter.converter.subprocess.Popen") as launch:
            self.assertEqual(self.run_converter(converter), -1)
            launch.assert_not_called()
        converter.prepare_current()
        process = FakeProcess()
        with patch("modules.converter.converter.subprocess.Popen", return_value=process):
            self.assertEqual(self.run_converter(converter), 0)
        self.assertIsNone(converter._process)
        self.assertFalse(converter.cancelled)

    def test_cancel_during_launch_terminates_published_process(self):
        converter = Converter()
        process = FakeProcess()
        def launch(*args, **kwargs):
            converter.cancel_current()
            return process
        with patch("modules.converter.converter.subprocess.Popen", side_effect=launch):
            self.assertEqual(self.run_converter(converter), -1)
        self.assertEqual(process.terminations, 1)
        self.assertIsNone(converter._process)
        self.assertTrue(process.stderr.closed)

    def test_active_cancel_and_cleanup_after_callback_error(self):
        converter = Converter()
        process = FakeProcess()
        monitor = Mock()
        def log(line):
            if line == "trigger":
                converter.cancel_current()
                raise RuntimeError("callback failure")
        process.stderr = io.StringIO("trigger\n")
        monitor.append_log.side_effect = log
        with patch("modules.converter.converter.subprocess.Popen", return_value=process):
            with self.assertRaises(RuntimeError):
                converter.execute(Path("input.mkv"), ConversionJob(), monitor=monitor)
        self.assertEqual(process.terminations, 1)
        self.assertIsNone(converter._process)
        self.assertTrue(process.stderr.closed)

    def test_launch_error_leaves_no_process(self):
        converter = Converter()
        with patch("modules.converter.converter.subprocess.Popen", side_effect=OSError("launch failed")):
            with self.assertRaises(OSError):
                self.run_converter(converter)
        self.assertIsNone(converter._process)
