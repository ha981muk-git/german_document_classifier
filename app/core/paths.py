# Project root directory
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Add project root for imports
sys.path.append(str(PROJECT_ROOT))

APP_DIR = PROJECT_ROOT / "app"

DATA_DIR = APP_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"

# Output directory (Where the CSV will go)
PROCESSED_DIR = DATA_DIR / "processed"


