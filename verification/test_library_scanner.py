from pathlib import Path

from modules.scanner.library_scanner import (
    LibraryScanner,
)


scanner = LibraryScanner()

episodes = scanner.scan_episodes(
    Path("data/samples")
)

print()

print(
    f"Episodios encontrados: {len(episodes)}"
)

print()

for episode in episodes:
    print(episode)