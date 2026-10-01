import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from core.models.audio_track import AudioTrack
from core.models.subtitle_track import SubtitleTrack
from core.models.video_track import VideoTrack
from core.models.media_item import MediaItem
from core.models.media_language import MediaLanguage
from modules.conversion.conversion_job_builder import ConversionJobBuilder
from modules.converter.converter import Converter
from modules.planning.conversion_planner import ConversionPlanner
from modules.validation.validation_service import ValidationService
from modules.validation.output_verifier import OutputVerifier
from services.conversion_service import ConversionService
from core.models.output_file import OutputFile


class SelectiveConversionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'output.mp4'
        self.path.write_bytes(b'output')
        self.video = VideoTrack('h264', 1920, 1080, 0, 24, 'High', 4.1, 'yuv420p', '', '')
        self.audios = [AudioTrack(i, codec, 2, 0, MediaLanguage(lang), lang, False, False)
                       for i, codec, lang in [(1, 'aac', 'spa'), (2, 'eac3', 'eng'), (3, 'aac', 'jpn')]]
        self.subs = [SubtitleTrack(i, codec, MediaLanguage(lang), lang, False, False)
                     for i, codec, lang in [(4, 'mov_text', 'spa'), (5, 'subrip', 'eng'), (6, 'subrip', 'jpn')]]
        self.source = MediaItem('source.mp4', Path(self.temp.name)/'source.mp4', 'mp4',
                                100, 6, 0, [self.video], self.audios, self.subs)
        self.settings = dict(audio_tracks=self.audios[:2], subtitle_tracks=self.subs[:2], default_audio_track=self.audios[0])
        self.builder = ConversionJobBuilder()
        self.plan = ConversionPlanner().plan(self.source, ValidationService().validate(self.source))
        self.job = self.builder.build(self.source, self.plan, self.settings)
        self.output = replace(self.source, path=self.path, audio_tracks=[replace(self.audios[0], default=True), replace(self.audios[1], codec='aac')],
                              subtitle_tracks=[replace(self.subs[0], default=True), replace(self.subs[1], codec='mov_text')])

    def test_mixed_copy_transcode_drop(self):
        command = Converter().build_command(self.source.path, self.job, self.path)
        for option, value in [('-c:v','copy'),('-c:a:0','copy'),('-c:a:1','aac'),('-c:s:0','copy'),('-c:s:1','mov_text')]:
            self.assertEqual(command[command.index(option)+1], value)
        maps = [command[i+1] for i, value in enumerate(command) if value == '-map']
        self.assertEqual(maps, ['0:V:0','0:1','0:2','0:4','0:5'])

    def test_main_remains_incompatible(self):
        source = replace(self.source, video_tracks=[replace(self.video, profile='Main')])
        plan = ConversionPlanner().plan(source, ValidationService().validate(source))
        job = self.builder.build(source, plan, self.settings)
        command = Converter().build_command(source.path, job, self.path)
        self.assertEqual(command[command.index('-c:v')+1], 'libx264')

    def test_empty_selection_preserves_all_audio_no_subtitles(self):
        job = self.builder.build(self.source, self.plan, dict(audio_tracks=[], subtitle_tracks=[]))
        self.assertEqual(job.audio_tracks, self.audios)
        self.assertFalse(job.include_subtitles)
        command = Converter().build_command(self.source.path, job, self.path)
        self.assertIn('0:3', command)
        self.assertNotIn('0:4', command)

    def test_exact_composition(self):
        verifier = OutputVerifier()
        self.assertTrue(verifier.verify(self.source, self.output, self.job).is_valid)
        variants = [replace(self.output, audio_tracks=list(reversed(self.output.audio_tracks))),
                    replace(self.output, audio_tracks=self.output.audio_tracks+[self.audios[2]]),
                    replace(self.output, subtitle_tracks=self.output.subtitle_tracks+[self.subs[2]]),
                    replace(self.output, audio_tracks=[replace(self.output.audio_tracks[0], default=False),self.output.audio_tracks[1]]),
                    replace(self.output, subtitle_tracks=[self.subs[0], self.subs[1]])]
        for output in variants:
            self.assertFalse(verifier.verify(self.source, output, self.job).is_valid)

    def service(self, output):
        service = ConversionService.__new__(ConversionService)
        service.converter = Mock(cancelled=False)
        service.converter.build_output_file.return_value = OutputFile(self.source.path,self.path,'mp4',True)
        service.converter.execute.return_value = 1
        service.media_service = Mock()
        service.media_service.get_media.side_effect = lambda path: self.source if path == self.source.path else output
        service.validation_service = ValidationService()
        service.output_verifier = OutputVerifier()
        service.conversion_planner = ConversionPlanner()
        service.conversion_job_builder = self.builder
        service.logger = Mock()
        return service

    def test_same_composition_skips(self):
        service = self.service(self.output)
        result = service.process_file(self.source.path,self.path,self.settings)
        self.assertTrue(result.skipped)
        service.converter.execute.assert_not_called()

    def test_different_composition_rebuilds_even_compatible_source(self):
        service = self.service(replace(self.output,audio_tracks=self.output.audio_tracks+[self.audios[2]]))
        with patch('services.conversion_service.copy2') as copy, patch('services.conversion_service.ConversionMonitor'):
            result = service.process_file(self.source.path,self.path,self.settings)
        self.assertFalse(result.skipped)
        copy.assert_not_called()
        service.converter.execute.assert_called_once()
        self.assertTrue(service.converter.execute.call_args.kwargs['overwrite'])
        job = service.converter.execute.call_args.args[1]
        self.assertFalse(job.convert_video)

    def test_copy_without_settings_checks_exact_composition(self):
        self.source = replace(self.source, audio_tracks=[replace(t, codec="aac") for t in self.audios],
                              subtitle_tracks=[replace(t, codec="mov_text") for t in self.subs])
        service = self.service(self.output)
        with patch('services.conversion_service.copy2') as copy:
            # Source is compatible, but the output omitted one source audio/subtitle.
            service.process_file(self.source.path, self.path)
        copy.assert_called_once()

    def test_secondary_incompatible_tracks_prevent_full_copy(self):
        service = self.service(self.output)
        with patch('services.conversion_service.copy2') as copy, patch('services.conversion_service.ConversionMonitor'):
            service.process_file(self.source.path, self.path)
        copy.assert_not_called()
        service.converter.execute.assert_called_once()
        self.assertEqual(service.converter.execute.call_args.args[1].audio_codecs[2], 'aac')

    def test_container_metadata_not_required_for_composition(self):
        output = replace(self.output, audio_tracks=[replace(t, title="") for t in self.output.audio_tracks],
                         subtitle_tracks=[replace(t, title="") for t in self.output.subtitle_tracks])
        self.assertTrue(OutputVerifier().verify(self.source, output, self.job).is_valid)

    def test_service_nvenc_selection_reaches_transcode_job(self):
        self.source = replace(self.source, video_tracks=[replace(self.video, profile="Main")])
        service = self.service(self.output)
        self.path.unlink()
        settings = dict(self.settings, video_encoder="h264_nvenc")
        with patch('services.conversion_service.ConversionMonitor'):
            service.process_file(self.source.path, self.path, settings)
        job = service.converter.execute.call_args.args[1]
        self.assertEqual(job.target_video_codec, "h264_nvenc")
        self.assertIn("-cq", job.video_encoder_options)

    def test_service_nvenc_selection_leaves_copy_and_tracks_intact(self):
        output = replace(self.output, audio_tracks=self.output.audio_tracks + [self.audios[2]])
        service = self.service(output)
        with patch('services.conversion_service.ConversionMonitor'):
            service.process_file(self.source.path, self.path, dict(self.settings, video_encoder="h264_nvenc"))
        job = service.converter.execute.call_args.args[1]
        command = Converter().build_command(self.source.path, job, self.path)
        self.assertEqual(command[command.index("-c:v") + 1], "copy")
        self.assertNotIn("-preset", command)
        self.assertEqual(job.audio_tracks, self.job.audio_tracks)
        self.assertEqual(job.subtitle_tracks, self.job.subtitle_tracks)
        self.assertEqual(job.audio_codecs, self.job.audio_codecs)
        self.assertEqual(job.subtitle_codecs, self.job.subtitle_codecs)

    def test_builder_replaces_default_outside_selection(self):
        settings = dict(self.settings, audio_tracks=[self.audios[1]], default_audio_track=self.audios[0])
        job = self.builder.build(self.source, self.plan, settings)
        self.assertEqual(job.audio_tracks, [self.audios[1]])
        self.assertIs(job.default_audio_track, self.audios[1])

    def test_default_order_and_flags(self):
        selected = dict(self.settings, default_audio_track=self.audios[1])
        job = self.builder.build(self.source,self.plan,selected)
        self.assertEqual(job.audio_tracks,[self.audios[1],self.audios[0]])
        command = Converter().build_command(self.source.path,job,self.path)
        self.assertEqual(command[command.index('-c:a:0')+1],'aac')
        self.assertEqual(command[command.index('-c:a:1')+1],'copy')


class VideoEncoderWidgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        cls.app = QApplication.instance() or QApplication([])

    def test_default_nvenc_and_cpu_only_change_encoder_setting(self):
        from app.widgets.conversion_setup_widget import ConversionSetupWidget
        widget = ConversionSetupWidget()
        try:
            before = widget.conversion_settings()
            self.assertEqual(before["video_encoder"], "h264_nvenc")
            widget.video_encoder_combo.setCurrentIndex(0)
            after = widget.conversion_settings()
            self.assertEqual(after["video_encoder"], "libx264")
            self.assertEqual({k: v for k, v in before.items() if k != "video_encoder"},
                             {k: v for k, v in after.items() if k != "video_encoder"})
        finally:
            widget.deleteLater()


    def test_deselect_default_selects_first_remaining_and_syncs_radio(self):
        self.check_audio_deselection(two_tracks=True)

    def test_deselect_only_audio_clears_default_and_radio(self):
        self.check_audio_deselection(two_tracks=False)

    def check_audio_deselection(self, two_tracks):
        from app.widgets.conversion_setup_widget import ConversionSetupWidget
        fixture = SelectiveConversionTests()
        fixture.setUp()
        widget = ConversionSetupWidget()
        try:
            tracks = fixture.audios[:2] if two_tracks else fixture.audios[:1]
            widget.load_selection([replace(fixture.source, audio_tracks=tracks)])
            radios = widget._audio_group.buttons()
            self.assertTrue(radios[0].isChecked())
            widget._audio_checkboxes[0].setChecked(False)
            self.assertFalse(radios[0].isChecked())
            self.assertFalse(radios[0].isEnabled())
            settings = widget.conversion_settings()
            if two_tracks:
                self.assertEqual(settings["audio_tracks"], [tracks[1]])
                self.assertIs(settings["default_audio_track"], tracks[1])
                self.assertTrue(radios[1].isChecked())
            else:
                self.assertEqual(settings["audio_tracks"], [])
                self.assertIsNone(settings["default_audio_track"])
                widget._audio_checkboxes[0].setChecked(True)
                self.assertTrue(radios[0].isChecked())
                self.assertIs(widget.conversion_settings()["default_audio_track"], tracks[0])
        finally:
            widget.deleteLater()
            fixture.temp.cleanup()


if __name__ == '__main__':
    unittest.main()
