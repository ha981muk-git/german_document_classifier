import sys
from pathlib import Path
import pandas as pd

from core.paths import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR
from src.prepare_data import process_dataset
from src.train import train_model
from src.evaluate import evaluate_model
import argparse

# -----------------------------
# Configuration
# -----------------------------

LABEL_MAP = {
    "complaints": "complaint",
    "contracts": "contract",
    "invoices": "invoice",
    "orders": "order",
    "paymentreminders": "reminder",
}

MODELS = [
    "deepset/gbert-base",
    "dbmdz/bert-base-german-cased",
]


# -----------------------------
# Helpers
# -----------------------------

def combine_csv_files(processed_dir: Path) -> Path:
    """Combine all CSV files in PROCESSED_DIR into all_data.csv."""
    csv_files = list(processed_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in PROCESSED_DIR.")

    df_list = [pd.read_csv(f) for f in csv_files]
    all_data = pd.concat(df_list, ignore_index=True)

    output_csv = processed_dir / "all_data.csv"

    if not output_csv.exists():
        all_data.to_csv(output_csv, index=False)
        print(f"Created combined CSV: {output_csv}")
    else:
        print(f"Using existing CSV: {output_csv}")

    print(f"Combined {len(csv_files)} CSV files into {output_csv}")
    return output_csv


def prepare_datasets():
    """Optional dataset preparation (commented out in your current version)."""

    raw_csv = Path(PROCESSED_DIR) / "raw_data.csv"
    process_dataset(RAW_DIR, str(raw_csv), LABEL_MAP)

    if SYNTHETIC_DIR is not None:
        synthetic_csv = Path(PROCESSED_DIR) / "synthetic_data.csv"
        process_dataset(SYNTHETIC_DIR, str(synthetic_csv), LABEL_MAP)


# -----------------------------
# Main Training Loop
# -----------------------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Run dataset preparation")
    args = parser.parse_args()

    if args.prepare:
        print("Preparing datasets...")
        prepare_datasets()


    processed_dir = Path(PROCESSED_DIR)
    csv_path = combine_csv_files(processed_dir)
    csv_path = str(csv_path)  # convert to string for model functions

    results = {}

    for model_name in MODELS:
        print(f"\n🚀 Training {model_name}")

        save_path = str(PROJECT_ROOT / "models" / model_name.replace("/", "_"))

        train_metrics = train_model(
            model_name=model_name,
            csv_path=csv_path,
            save_path=save_path,
            learning_rate=3e-5,
            epochs=10
        )

        print("\nTraining metrics:")
        print(train_metrics)

        print("\n🔍 Evaluating on test set...")
        eval_metrics = evaluate_model(save_path, csv_path)

        print("Evaluation metrics:")
        print(eval_metrics)

        results[model_name] = {"train": train_metrics, "eval": eval_metrics}

    print("\n📊 Final model results:")
    for model, metrics in results.items():
        print(f"\nMODEL: {model}")
        print(metrics)


if __name__ == "__main__":
    main()
