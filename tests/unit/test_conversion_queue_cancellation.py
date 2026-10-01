import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication

from app.windows import main_window
from core.models.media_item import MediaItem
from core.models.process_result import ProcessResult
from core.models.scan_result import ScanResult

RealConversionWorker = main_window.ConversionWorker


class FakeWorker(QObject):
    result_ready = Signal(object, object)
    progress_updated = Signal(object)
    finished = Signal()

    def __init__(self, service, item, output, settings):
        super().__init__()
        service.prepare_current()
        self._media_item = item
        self._output_path = output
        self.result = None
        self.deleted = False
        self.started = False

    def start(self):
        self.started = True

    def deleteLater(self):
        self.deleted = True

    def publish(self, result):
        self.result = result
        self.result_ready.emit(self._media_item, result)


class ConversionQueueCancellationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.service = Mock(cancelled=False)
        settings = Mock()
        settings.value.side_effect = lambda key, default, **kwargs: default
        for name, value in (("ConversionService", self.service), ("QSettings", settings)):
            patcher = patch.object(main_window, name, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(main_window, "ConversionWorker", FakeWorker)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.window = main_window.MainWindow()
        self.addCleanup(self.window.deleteLater)
        self.first = MediaItem("one.mkv", Path("one.mkv"), "mkv", 10.0, 1, 1, [], [], [])
        self.second = MediaItem("two.mkv", Path("two.mkv"), "mkv", 10.0, 1, 1, [], [], [])
        self.console = self.window.control_console
        self.console.add_media_items([self.first, self.second], {
            self.first.path: Path("one.mp4"), self.second.path: Path("two.mp4"),
        })

    def test_cancel_stops_queue_preserves_pending_and_resumes(self):
        self.assertTrue(self.console.start_button.isEnabled())
        self.assertFalse(self.console.cancel_button.isEnabled())
        self.window._start_queue()
        worker = self.window._conversion_worker
        self.assertFalse(self.console.start_button.isEnabled())
        self.assertTrue(self.console.cancel_button.isEnabled())
        def cancel():
            self.assertFalse(self.window._queue_running)
            self.assertTrue(self.window._queue_stopped_by_cancel)
        self.service.cancel_current.side_effect = cancel
        self.console.cancel_button.click()
        self.assertFalse(self.console.cancel_button.isEnabled())
        self.assertFalse(self.console.start_button.isEnabled())
        # Even a success racing with the user's request must not advance queue.
        worker.publish(ProcessResult(success=True))
        self.assertFalse(worker.deleted)
        self.assertIs(self.window._conversion_worker, worker)
        self.assertFalse(self.console.start_button.isEnabled())
        worker.finished.emit()
        self.assertTrue(worker.deleted)
        self.assertIsNone(self.window._conversion_worker)
        self.assertEqual([entry["state"] for entry in self.console._queue], ["Cancelled", "Queued"])
        self.assertTrue(self.console.start_button.isEnabled())
        self.assertFalse(self.console.cancel_button.isEnabled())
        self.console.start_button.click()
        resumed = self.window._conversion_worker
        self.assertIs(resumed._media_item, self.second)
        self.assertFalse(self.window._queue_stopped_by_cancel)
        resumed.publish(ProcessResult(success=True))
        resumed.finished.emit()
        self.assertIsNone(self.window._conversion_worker)

    def test_normal_queue_advances_only_after_thread_finished(self):
        self.window._start_queue()
        worker = self.window._conversion_worker
        worker.publish(ProcessResult(success=True))
        self.assertIs(self.window._conversion_worker, worker)
        self.assertFalse(worker.deleted)
        worker.finished.emit()
        self.assertTrue(worker.deleted)
        next_worker = self.window._conversion_worker
        self.assertIs(next_worker._media_item, self.second)
        next_worker.publish(ProcessResult(success=True))
        next_worker.finished.emit()

    def test_close_cancels_and_waits_for_finished(self):
        self.window._start_queue()
        worker = self.window._conversion_worker
        event = QCloseEvent()
        self.window.closeEvent(event)
        self.assertFalse(event.isAccepted())
        self.assertTrue(self.window._close_pending)
        self.service.cancel_current.assert_called_once()
        with patch.object(self.window, "close") as close:
            worker.publish(ProcessResult(success=False, cancelled=True))
            close.assert_not_called()
            self.assertFalse(worker.deleted)
            worker.finished.emit()
            close.assert_called_once()
        self.assertEqual(self.console._queue[1]["state"], "Queued")
        final = QCloseEvent()
        self.window.closeEvent(final)
        self.assertTrue(final.isAccepted())

    def test_worker_preserves_explicit_cancelled_result(self):
        self.service.cancelled = True
        self.service.process_file.return_value = ProcessResult(success=True)
        worker = RealConversionWorker(self.service, self.first, Path("one.mp4"), {})
        worker.run()
        self.assertTrue(worker.result.cancelled)
        self.assertFalse(worker.result.success)
        self.service.prepare_current.assert_called_once()

    def test_cancelled_flag_defaults_false(self):
        self.assertFalse(ProcessResult(success=True).cancelled)

    def test_close_waits_for_both_workers_in_either_order(self):
        for scan_first in (True, False):
            with self.subTest(scan_first=scan_first):
                self.window._close_pending = False
                self.window._start_queue()
                conversion = self.window._conversion_worker
                scan = Mock(result=ScanResult())
                self.window._library_scan_worker = scan
                event = QCloseEvent()
                self.window.closeEvent(event)
                self.assertFalse(event.isAccepted())
                with patch.object(self.window, "close") as close:
                    if scan_first:
                        self.window._on_library_scan_finished()
                        close.assert_not_called()
                    conversion.publish(ProcessResult(success=False, cancelled=True))
                    conversion.finished.emit()
                    if not scan_first:
                        close.assert_not_called()
                        self.window._on_library_scan_finished()
                    close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
