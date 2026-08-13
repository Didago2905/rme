from pathlib import Path

from core.models.analysis_result import AnalysisResult
from core.models.audio_track import AudioTrack
from core.models.media_item import MediaItem
from core.models.subtitle_track import SubtitleTrack
from core.models.video_track import VideoTrack
from core.models.media_language import MediaLanguage
from services.ffmpeg_service import FFmpegService


class Analyzer:
    def __init__(self):
        self.ffmpeg = FFmpegService()

    def analyze(self, file_path: Path) -> AnalysisResult:
        media_info = self.ffmpeg.get_media_info(file_path)

        video_tracks = []
        audio_tracks = []
        subtitle_tracks = []

        for stream in media_info.get("streams", []):
            stream_type = stream.get("codec_type")

            if stream_type == "video":
                fps = 0.0

                fps_string = stream.get("avg_frame_rate", "0/1")

                try:
                    numerator, denominator = fps_string.split("/")
                    fps = float(numerator) / float(denominator)
                except (ValueError, ZeroDivisionError):
                    pass

                raw_level = stream.get("level")

                level = None
                if raw_level is not None:
                    try:
                        level = float(raw_level) / 10
                    except (TypeError, ValueError):
                        level = None

                video_tracks.append(
                    VideoTrack(
                        codec=stream.get("codec_name", ""),
                        width=stream.get("width", 0),
                        height=stream.get("height", 0),
                        bitrate=int(
                            stream.get(
                                "bit_rate",
                                stream.get("tags", {}).get("BPS", 0),
                            )
                        ),
                        fps=fps,
                        profile=stream.get("profile", ""),
                        level=level,
                        pixel_format=stream.get("pix_fmt", ""),
                        color_space=stream.get("color_space", ""),
                        field_order=stream.get("field_order", ""),
                    )
                )

            elif stream_type == "audio":
                disposition = stream.get("disposition", {})
                tags = stream.get("tags", {})

                audio_tracks.append(
                    AudioTrack(
                        stream_index=stream.get("index", -1),
                        codec=stream.get("codec_name", ""),
                        language=MediaLanguage(
                            code=tags.get("language", ""),
                        ),
                        channels=stream.get("channels", 0),
                        bitrate=int(stream.get("bit_rate", 0)),
                        title=tags.get(
                            "title",
                            tags.get("name", ""),
                        ),
                        default=bool(
                            disposition.get("default", 0)
                        ),
                        forced=bool(
                            disposition.get("forced", 0)
                        ),
                    )
                )

            elif stream_type == "subtitle":
                disposition = stream.get("disposition", {})
                tags = stream.get("tags", {})

                subtitle_tracks.append(
                    SubtitleTrack(
                        stream_index=stream.get("index", -1),
                        codec=stream.get("codec_name", ""),
                        language=MediaLanguage(
                            code=tags.get("language", ""),
                        ),
                        title=tags.get(
                            "title",
                            tags.get("name", ""),
                        ),
                        default=bool(
                            disposition.get("default", 0)
                        ),
                        forced=bool(
                            disposition.get("forced", 0)
                        ),
                    )
                )

        media_item = MediaItem(
            file_name=file_path.name,
            path=file_path,
            container=file_path.suffix.lower().lstrip("."),
            duration_seconds=float(
                media_info.get("format", {}).get(
                    "duration",
                    0.0,
                )
            ),
            size_bytes=file_path.stat().st_size,
            bitrate=int(
                media_info.get("format", {}).get(
                    "bit_rate",
                    0,
                )
            ),
            video_tracks=video_tracks,
            audio_tracks=audio_tracks,
            subtitle_tracks=subtitle_tracks,
        )

        return AnalysisResult(
            media_item=media_item,
            success=True,
            analyzer="ffprobe",
        )