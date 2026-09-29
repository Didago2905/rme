from pathlib import Path
from unittest.mock import patch

from app.use_cases.scan_library import ScanLibraryUseCase
from core.models.media_item import MediaItem
from core.models.scan_result import ScanRoot
from core.models.video_track import VideoTrack
from modules.media.media_service import MediaService


def make_file(root: Path, relative: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"test media placeholder")
    return path


def media(path: Path, empty: bool = False) -> MediaItem:
    return MediaItem(
        file_name=path.name, path=path, container=path.suffix[1:],
        duration_seconds=1.0, size_bytes=22, bitrate=0,
        video_tracks=[] if empty else [VideoTrack(
            codec="h264", width=1920, height=1080, bitrate=0, fps=24.0,
            profile="High", level=4.1, pixel_format="yuv420p",
            color_space="bt709", field_order="progressive",
        )],
        audio_tracks=[], subtitle_tracks=[],
    )


def test_movies_and_series_only(tmp_path):
    movie = make_file(tmp_path, "Movies/Film/Film.M4V")
    episode = make_file(tmp_path, "Series/Show/Season 01/Episode.mkv")
    make_file(tmp_path, "Other/ignored.mp4")
    make_file(tmp_path, "Movies/Film/poster.jpg")
    make_file(tmp_path, "ignored.mp4")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}

    with patch.object(MediaService, "get_media", side_effect=media) as analyze:
        result = ScanLibraryUseCase().execute([ScanRoot("library", tmp_path)])

    assert [(i.relative_path, i.category) for i in result.items] == [
        (movie.relative_to(tmp_path), "movie"),
        (episode.relative_to(tmp_path), "series"),
    ]
    assert all(i.media_item is not None for i in result.items)
    assert analyze.call_count == 2
    assert result.anomalies == []
    assert result.roots[0].status == "complete"
    assert before == {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}


def test_analysis_failure_preserves_file_and_continues(tmp_path):
    failed = make_file(tmp_path, "Movies/a.mkv")
    good = make_file(tmp_path, "Movies/b.mp4")

    def analyze(path):
        if path == failed:
            raise RuntimeError("probe failed")
        return media(path)

    with patch.object(MediaService, "get_media", side_effect=analyze):
        result = ScanLibraryUseCase().execute([ScanRoot("root", tmp_path)])

    assert len(result.items) == 2
    assert result.items[0].media_item is None
    assert result.items[1].media_item.path == good
    assert result.anomalies[0].code == "analysis_failed"
    assert result.anomalies[0].relative_path == failed.relative_to(tmp_path)
    assert result.anomalies[0].detail == "probe failed"
    assert result.roots[0].status == "complete"


def test_empty_analysis_is_retained_with_anomaly(tmp_path):
    path = make_file(tmp_path, "Movies/empty.mp4")
    empty = media(path, empty=True)
    with patch.object(MediaService, "get_media", return_value=empty):
        result = ScanLibraryUseCase().execute([ScanRoot("root", tmp_path)])

    assert result.items[0].media_item is empty
    assert len(result.anomalies) == 1
    assert result.anomalies[0].code == "analysis_empty"
    assert result.anomalies[0].root_id == "root"
    assert result.anomalies[0].relative_path == Path("Movies/empty.mp4")


def test_multiple_roots_keep_logical_ids_and_relative_paths(tmp_path):
    roots = [ScanRoot("primary", tmp_path / "disk_a"),
             ScanRoot("archive", tmp_path / "disk_b")]
    for root in roots:
        make_file(root.path, "Series/Show/episode.mkv")

    with patch.object(MediaService, "get_media", side_effect=media):
        result = ScanLibraryUseCase().execute(roots)

    assert [(r.root_id, r.path, r.status) for r in result.roots] == [
        (r.root_id, r.path, "complete") for r in roots
    ]
    assert [(i.root_id, i.relative_path) for i in result.items] == [
        (r.root_id, Path("Series/Show/episode.mkv")) for r in roots
    ]
    assert [i.media_item.path for i in result.items] == [
        r.path / "Series/Show/episode.mkv" for r in roots
    ]
    assert result.anomalies == []
