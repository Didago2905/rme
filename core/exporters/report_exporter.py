from pathlib import Path

from core.models.library_metadata import (
    LibraryMetadata,
)


class ReportExporter:

    @staticmethod
    def export_library(
        library: LibraryMetadata,
        output_path: Path,
    ) -> None:

        lines = []

        lines.append(
            "========================================"
        )

        lines.append(
            "RME LIBRARY REPORT"
        )

        lines.append(
            "========================================"
        )

        lines.append("")

        lines.append(
            f"Series: {len(library.series)}"
        )

        lines.append("")

        for series in library.series:

            lines.append(
                "----------------------------------------"
            )

            lines.append(
                series.name
            )

            lines.append(
                "----------------------------------------"
            )

            lines.append("")

            for season in series.seasons:

                lines.append(
                    f"Season {season.season_number:02d}"
                )

                lines.append("")

                lines.append(
                    f"Episodes Present : {len(season.episodes)}"
                )

                lines.append(
                    f"Episodes Missing : {len(season.missing_episodes)}"
                )

                lines.append("")

                lines.append("Present:")

                for episode in season.episodes:

                    lines.append(
                        f"E{episode.episode_number:02d}"
                    )

                lines.append("")

                lines.append("Missing:")

                if season.missing_episodes:

                    for missing in season.missing_episodes:

                        lines.append(
                            f"E{missing.episode_number:02d}"
                        )

                else:

                    lines.append(
                        "None"
                    )

                lines.append("")
                lines.append("")

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )