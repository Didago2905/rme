from modules.batch.batch_stats import BatchStats


class BatchReport:

    @staticmethod
    def build(
        stats: BatchStats,
    ) -> str:

        lines = []

        lines.append("")
        lines.append("===== BATCH REPORT =====")
        lines.append("")

        lines.append(
            f"Total Files : {stats.total_files}"
        )

        lines.append(
            f"Processed   : {stats.processed}"
        )

        lines.append(
            f"Skipped     : {stats.skipped}"
        )

        lines.append(
            f"Failed      : {stats.failed}"
        )

        failed_results = [
            result
            for result in stats.results
            if not result.success
        ]

        if failed_results:

            lines.append("")
            lines.append("FAILED FILES")
            lines.append("")

            for result in failed_results:

                lines.append(
                    f"- {result.file_path.name}"
                )

                if result.error:

                    lines.append(
                        f"  Error: {result.error}"
                    )

        lines.append("")

        return "\n".join(lines)