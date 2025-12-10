import sys
from pathlib import Path

# --------------------------------------------------------
# Project Root
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Make project importable (optional but safe)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --------------------------------------------------------
# Directory Structure
# --------------------------------------------------------

APP_DIR = PROJECT_ROOT / "app"
DATA_DIR = APP_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
PROCESSED_DIR = DATA_DIR / "processed"

DIRS_TO_CREATE = [RAW_DIR, SYNTHETIC_DIR, PROCESSED_DIR]

# Automatically create directories if missing
for d in DIRS_TO_CREATE:
    d.mkdir(parents=True, exist_ok=True)
