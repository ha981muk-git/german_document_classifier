# Project root directory
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_DIR = PROJECT_ROOT / "app"


# Add project root for imports
sys.path.append(str(PROJECT_ROOT))


DATA_DIR = APP_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"

# Output directory (Where the CSV will go)
PROCESSED_DIR = DATA_DIR / "processed"

# OUTPUT_FILENAME = "labeled_documents.csv"

# Mapping Directory Names -> Target Labels
# Key = Folder Name, Value = Label for CSV
LABEL_MAP = {
    "complaints": "complaint",
    "contracts": "contract",
    "invoices": "invoice",
    "orders": "order",
    "paymentreminders": "reminder"
}