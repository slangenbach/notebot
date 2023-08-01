"""Package wide constants."""
from pathlib import Path
from typing import Final

ROOT_PATH: Final = Path(__file__).parent.parent
DATA_PATH: Final = ROOT_PATH / "data"
NOTES_PATH: Final = DATA_PATH / "notes"
DB_PATH: Final = DATA_PATH / "db"

NOTE_REPO_URL: Final = "https://github.com/slangenbach/notes.git"
