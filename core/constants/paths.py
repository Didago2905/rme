import os
from pathlib import Path


PROJECT_ROOT = Path.cwd()

DATA_DIR = PROJECT_ROOT / "data"

TEMP_DIR = DATA_DIR / "temp"

OUTPUT_DIR = DATA_DIR / "output"

LOGS_DIR = PROJECT_ROOT / "logs"

APP_STATE_DIR = (
    Path(os.environ["LOCALAPPDATA"]) / "RITMO" / "RME"
    if os.name == "nt" and os.environ.get("LOCALAPPDATA")
    else Path.home() / ".ritmo" / "rme"
)

LIBRARY_INDEX_PATH = APP_STATE_DIR / "library_index.sqlite3"
