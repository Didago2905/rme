from pathlib import Path

from core.models.analysis_result import AnalysisResult
from core.models.audio_track import AudioTrack
from core.models.media_file import MediaFile
from core.models.video_track import VideoTrack
from services.ffmpeg_service import FFmpegService
from core.models.subtitle_track import SubtitleTrack


class Analyzer:
    def __init__(self):
        self.ffmpeg = FFmpegService()

    def analyze(self, file_path: Path) -> AnalysisResult:
        media_info = self.ffmpeg.get_media_info(file_path)

        media_file = MediaFile(
            path=file_path,
            file_name=file_path.name,
            container=file_path.suffix.lower().lstrip("."),
            size_bytes=file_path.stat().st_size,
            duration_seconds=float(media_info.get("format", {}).get("duration", 0.0)),
        )

        for stream in media_info.get("streams", []):
            stream_type = stream.get("codec_type")

            if stream_type == "video":
                fps = 0.0

                fps_string = stream.get("avg_frame_rate", "0/1")

                try:
                    numerator, denominator = fps_string.split("/")
                    fps = float(numerator) / float(denominator)
                except Exception:
                    pass

                media_file.video_tracks.append(
                    VideoTrack(
                        codec=stream.get("codec_name", ""),
                        width=stream.get("width", 0),
                        height=stream.get("height", 0),
                        bitrate=int(
                            stream.get("bit_rate", stream.get("tags", {}).get("BPS", 0))
                        ),
                        fps=fps,
                        profile=stream.get("profile", ""),
                        pixel_format=stream.get("pix_fmt", ""),
                        color_space=stream.get("color_space", ""),
                    )
                )

            elif stream_type == "audio":
                disposition = stream.get("disposition", {})

                media_file.audio_tracks.append(
                    AudioTrack(
                        codec=stream.get("codec_name", ""),
                        language=stream.get("tags", {}).get("language", ""),
                        channels=stream.get("channels", 0),
                        bitrate=int(stream.get("bit_rate", 0)),
                        default=bool(disposition.get("default", 0)),
                        forced=bool(disposition.get("forced", 0)),
                    )
                )
            elif stream_type == "subtitle":
                media_file.subtitle_tracks.append(
                    SubtitleTrack(
                        codec=stream.get("codec_name", ""),
                        language=stream.get("tags", {}).get("language", ""),
                    )
                )
        return AnalysisResult(
            media_file=media_file,
            success=True,
            analyzer="ffprobe",
        )
