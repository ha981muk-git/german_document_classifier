import sys
# First app import to ensure PROJECT_ROOT is added to sys.path
from app.core.paths import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR
from pathlib import Path
from typing import Dict, List
import pandas as pd

from app.core.utils import extract_pdf, clean_text


def read_text_file(path: Path) -> str:
    """Read a TXT file with fallback encodings."""
    for encoding in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[ERROR] Cannot read {path}: {e}", file=sys.stderr)
            return ""
    print(f"[WARN] Could not decode text file: {path}", file=sys.stderr)
    return ""


def process_dataset(input_dir: str, output_file: str, label_map: Dict[str, str]) -> pd.DataFrame | None:
    """Walk through folders, extract PDF/TXT text, clean it, assign labels, and export CSV."""
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting dataset processing: {input_path}")

    records: List[dict] = []

    for class_folder, label in label_map.items():
        folder_path = input_path / class_folder

        if not folder_path.is_dir():
            print(f"[WARN] Missing directory: {folder_path}", file=sys.stderr)
            continue

        print(f"→ Processing: {class_folder}  (label={label})")

        files = [f for f in folder_path.iterdir() if f.suffix.lower() in {".pdf", ".txt"}]
        total_files = len(files)

        for idx, file in enumerate(files, start=1):
            text_raw = extract_pdf(str(file)) if file.suffix.lower() == ".pdf" else read_text_file(file)
            text_clean = clean_text(text_raw)

            if text_clean:
                records.append({
                    "filename": file.name,
                    "text": text_clean,
                    "label": label
                })

            # Print progress every 25 files
            if idx % 25 == 0 or idx == total_files:
                print(f"   Processed {idx}/{total_files} files...")

    if not records:
        print(f"[EMPTY] No documents extracted from {input_dir}", file=sys.stderr)
        return None

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    print(f"\n✅ Completed: {len(df)} documents")
    print(f"📄 Saved CSV: {output_path}")
    print("\n📊 Label distribution:")
    print(df["label"].value_counts())

    return df


# -----------------------------
# Helpers
# -----------------------------

def combine_csv_files(processed_dir: Path) -> Path:
    """Combine all CSV files in PROCESSED_DIR into all_data.csv."""
    if not processed_dir.exists():
        raise FileNotFoundError(f"Processed directory not found: {processed_dir}")

    csv_files = list(processed_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in PROCESSED_DIR.")

    output_csv = processed_dir / "all_data.csv"

    if output_csv.exists():
        print(f"Using existing combined CSV: {output_csv}")
    else:
        print(f"Combining {len(csv_files)} CSV files into {output_csv}...")
        df_list = [pd.read_csv(f) for f in csv_files]
        all_data = pd.concat(df_list, ignore_index=True)
        all_data.to_csv(output_csv, index=False)
        print(f"Created combined CSV: {output_csv}")

    return output_csv


def prepare_datasets(config: dict) -> None:
    """Process raw and synthetic data into separate CSV files."""

    raw_csv = Path(PROCESSED_DIR) / "raw_data.csv"
    process_dataset(RAW_DIR, str(raw_csv), config["label_map"])

    if SYNTHETIC_DIR is not None:
        synthetic_csv = Path(PROCESSED_DIR) / "synthetic_data.csv"
        process_dataset(SYNTHETIC_DIR, str(synthetic_csv), config["label_map"])
