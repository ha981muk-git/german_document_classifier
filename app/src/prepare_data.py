import os
from pathlib import Path
from typing import Dict, List
import pandas as pd

from app.core.paths import LABEL_MAP, PROCESSED_DIR, RAW_DIR, SYNTHETIC_DIR
from app.src.utils import extract_pdf, clean_text


def read_text_file(path: Path) -> str:
    """Read a TXT file with fallback encodings."""
    for encoding in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[ERROR] Cannot read {path}: {e}")
            return ""
    print(f"[WARN] Could not decode text file: {path}")
    return ""


def process_dataset(input_dir: str, output_file: str, label_map: Dict[str, int]) -> pd.DataFrame | None:
    """Walk through folders, extract PDF/TXT text, clean it, assign labels, and export CSV."""
    input_path = Path(input_dir)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting dataset processing: {input_path}")

    records: List[dict] = []

    for class_folder, label in label_map.items():
        folder_path = input_path / class_folder

        if not folder_path.is_dir():
            print(f"[WARN] Missing directory: {folder_path}")
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

            # Print progress every 10 files
            if idx % 10 == 0 or idx == total_files:
                print(f"   Processed {idx}/{total_files} files...")

    if not records:
        print(f"[EMPTY] No documents extracted from {input_dir}")
        return None

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    print(f"\n✅ Completed: {len(df)} documents")
    print(f"📄 Saved CSV: {output_path}")
    print("\n📊 Label distribution:")
    print(df["label"].value_counts())

    return df


