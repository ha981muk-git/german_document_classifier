# Project root directory
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_DIR = PROJECT_ROOT / "app"


# Add project root for imports
sys.path.append(str(PROJECT_ROOT))
