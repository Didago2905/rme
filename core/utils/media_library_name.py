import re


def build_episode_filename(
    series_name: str,
    season_number: int,
    episode_number: int,
) -> str:
    normalized_series_name = re.sub(r"[^A-Za-z0-9]+", ".", series_name).strip(".")

    return f"{normalized_series_name}.S{season_number:02}E{episode_number:02}.mp4"
