from pathlib import Path

from services.conversion_service import ConversionService

from modules.batch.batch_result import BatchResult
from modules.batch.batch_stats import BatchStats


SUPPORTED_EXTENSIONS = {
    ".mkv",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
}


class BatchProcessor:

    def __init__(
        self,
        conversion_service: ConversionService,
    ):
        self._conversion_service = conversion_service

    def _find_media_files(
        self,
        folder_path: Path,
    ) -> list[Path]:

        files = []

        for file in folder_path.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower() in SUPPORTED_EXTENSIONS
            ):
                files.append(file)

        return sorted(files)

    def _process_file(
        self,
        file_path: Path,
    ) -> BatchResult:

        try:

            process_result = (
                self._conversion_service.process_file(
                    file_path
                )
            )

            return BatchResult(
                file_path=file_path,
                success=process_result.success,
                skipped=process_result.skipped,
                output_path=process_result.output_path,
                error=process_result.error,
            )

        except Exception as e:

            return BatchResult(
                file_path=file_path,
                success=False,
                error=str(e),
            )

    def process_folder(
        self,
        folder_path: Path,
    ) -> BatchStats:

        media_files = self._find_media_files(
            folder_path
        )

        stats = BatchStats()

        stats.total_files = len(media_files)

        print()
        print(
            f"📂 Encontrados "
            f"{stats.total_files} archivos multimedia"
        )

        for file_path in media_files:

            result = self._process_file(
                file_path
            )

            stats.results.append(
                result
            )

            if result.skipped:
                stats.skipped += 1

            elif result.success:
                stats.processed += 1

            else:
                stats.failed += 1

        return stats

    def process_library(
        self,
        library_path: Path,
    ) -> BatchStats:

        stats = BatchStats()

        media_files = self._find_media_files(
            library_path
        )

        stats.total_files = len(
            media_files
        )

        print()
        print(
            "📚 Biblioteca escaneada"
        )

        print(
            f"📂 Archivos encontrados: "
            f"{stats.total_files}"
        )

        return stats