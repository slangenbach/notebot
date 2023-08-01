"""Package wide constants."""
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DATA_PATH = ROOT_PATH / "data"
NOTES_PATH = DATA_PATH / "notes"
DB_PATH = DATA_PATH / "db"

NOTE_REPO_URL = "https://github.com/slangenbach/notes.git"
