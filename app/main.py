import sys
from pathlib import Path
import pandas as pd
from collections import defaultdict

from core.paths import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR
from src.prepare_data import process_dataset
from src.train import train_model
from src.evaluate import evaluate_model
import argparse

# -----------------------------
# Configuration
# -----------------------------

class Config:
    """Configuration for the training pipeline."""
    LABEL_MAP = {
        "complaints": "complaint",
        "contracts": "contract",
        "invoices": "invoice",
        "orders": "order",
        "paymentreminders": "reminder",
    }
    MODELS_TO_TRAIN = [
        "deepset/gbert-base",
        "dbmdz/bert-base-german-cased",
    ]
    LEARNING_RATE = 3e-5
    EPOCHS = 10


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


def prepare_datasets() -> None:
    """Optional dataset preparation (commented out in your current version)."""

    raw_csv = Path(PROCESSED_DIR) / "raw_data.csv"
    process_dataset(RAW_DIR, str(raw_csv), Config.LABEL_MAP)

    if SYNTHETIC_DIR is not None:
        synthetic_csv = Path(PROCESSED_DIR) / "synthetic_data.csv"
        process_dataset(SYNTHETIC_DIR, str(synthetic_csv), Config.LABEL_MAP)


# -----------------------------
# Main Training Loop
# -----------------------------

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Run dataset preparation")
    args = parser.parse_args()

    if args.prepare:
        print("Preparing datasets from files ...")
        prepare_datasets()


    processed_dir = Path(PROCESSED_DIR)
    csv_path = combine_csv_files(processed_dir)

    results = defaultdict(dict)

    for model_name in Config.MODELS_TO_TRAIN:
        print(f"\n🚀 Training {model_name}")

        save_path = str(PROJECT_ROOT / "models" / model_name.replace("/", "_"))

        train_metrics = train_model(
            model_name=model_name,
            csv_path=str(csv_path),
            save_path=save_path,
            learning_rate=Config.LEARNING_RATE,
            epochs=Config.EPOCHS
        )

        print(f"\nTraining metrics for {model_name}:")
        print(train_metrics)
        results[model_name]["train"] = train_metrics

        print(f"\n🔍 Evaluating {model_name} on test set...")
        eval_metrics = evaluate_model(save_path, str(csv_path))

        print(f"Evaluation metrics for {model_name}:")
        print(eval_metrics)
        results[model_name]["eval"] = eval_metrics

    print("\n📊 Final model results summary:")
    for model, metrics in results.items():
        print(f"\n--- MODEL: {model} ---")
        print("  Training Metrics:", metrics.get("train", "N/A"))
        print("  Evaluation Metrics:", metrics.get("eval", "N/A"))
        print("--------------------" + "-" * len(model))


if __name__ == "__main__":
    main()
