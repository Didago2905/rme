from core.models.media_file import (
    MediaFile,
)

from core.models.video_track import (
    VideoTrack,
)

from core.models.audio_track import (
    AudioTrack,
)

from core.models.subtitle_track import (
    SubtitleTrack,
)

from core.utils.video_level import normalize_video_level


class MediaBuilder:

    def build(
        self,
        data: dict,
    ) -> MediaFile:

        format_info = data["format"]

        video_tracks = []

        audio_tracks = []

        subtitle_tracks = []

        for stream in data["streams"]:

            codec_type = stream.get("codec_type")

            if codec_type == "video":

                video_tracks.append(
                    VideoTrack(
                        codec=stream.get(
                            "codec_name",
                            "",
                        ),
                        width=stream.get(
                            "width",
                            0,
                        ),
                        height=stream.get(
                            "height",
                            0,
                        ),
                        frame_rate=stream.get(
                            "r_frame_rate",
                            "",
                        ),
                        pixel_format=stream.get(
                            "pix_fmt",
                            "",
                        ),
                        profile=stream.get(
                            "profile",
                            "",
                        ),
                        level=normalize_video_level(
                            codec=stream.get(
                                "codec_name",
                                "",
                            ),
                            raw_level=stream.get(
                                "level",
                            ),
                        ),
                        scan_type=stream.get(
                            "field_order",
                            "",
                        ),
                    )
                )

            elif codec_type == "audio":

                tags = stream.get("tags", {})

                audio_tracks.append(
                    AudioTrack(
                        codec=stream.get(
                            "codec_name",
                            "",
                        ),
                        channels=stream.get(
                            "channels",
                            0,
                        ),
                        language=tags.get(
                            "language",
                            "",
                        ),
                        title=tags.get(
                            "title",
                            "",
                        ),
                    )
                )

            elif codec_type == "subtitle":

                tags = stream.get("tags", {})

                subtitle_tracks.append(
                    SubtitleTrack(
                        codec=stream.get(
                            "codec_name",
                            "",
                        ),
                        language=tags.get(
                            "language",
                            "",
                        ),
                        title=tags.get(
                            "title",
                            "",
                        ),
                    )
                )

        return MediaFile(
            container=format_info.get(
                "format_name",
                "",
            ),
            duration_seconds=float(
                format_info.get(
                    "duration",
                    0,
                )
            ),
            size_bytes=int(
                format_info.get(
                    "size",
                    0,
                )
            ),
            bitrate=int(
                format_info.get(
                    "bit_rate",
                    0,
                )
            ),
            video_tracks=video_tracks,
            audio_tracks=audio_tracks,
            subtitle_tracks=subtitle_tracks,
        )
