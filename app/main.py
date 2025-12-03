# main.py
import sys

from src.prepare_data import process_dataset
from src.train import train_model
from src.evaluate import evaluate_model
from pathlib import Path
from core.paths import APP_DIR, PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR
from pathlib import Path
import pandas as pd

# Mapping Directory Names -> Target Labels
# Key = Folder Name, Value = Label for CSV
LABEL_MAP = {
    "complaints": "complaint",
    "contracts": "contract",
    "invoices": "invoice",
    "orders": "order",
    "paymentreminders": "reminder"
}

MODELS = [
    "deepset/gbert-base",
    "dbmdz/bert-base-german-cased",
]

"""
raw_csv = Path(PROCESSED_DIR) / "raw_data.csv"
process_dataset(RAW_DIR, str(raw_csv), LABEL_MAP)

if "SYNTHETIC_DIR" in globals():
    synthetic_csv = Path(PROCESSED_DIR) / "synthetic_data.csv"
    process_dataset(SYNTHETIC_DIR, str(synthetic_csv), LABEL_MAP)
"""

PROCESSED_DIR = Path(PROCESSED_DIR)
csv_files = list(PROCESSED_DIR.glob("*.csv"))  # all CSVs in the folder

# Combine into a single dataframe
df_list = [pd.read_csv(f) for f in csv_files]
all_data = pd.concat(df_list, ignore_index=True)

# Save combined CSV for training
CSV_PATH = PROCESSED_DIR / "all_data.csv"

if not CSV_PATH.exists():
    all_data.to_csv(CSV_PATH, index=False)
    print(f"Created combined CSV: {CSV_PATH}")
else:
    print(f"Using existing CSV: {CSV_PATH}")

print(f"Combined {len(csv_files)} CSV files into {CSV_PATH}")

CSV_PATH = str(CSV_PATH)

if __name__ == "__main__":
    results = {}

    for model_name in MODELS:
        print(f"🚀 Training {model_name}")

 
        save_path = str(PROJECT_ROOT / "models" / model_name.replace("/", "_"))


        # Train
        train_metrics = train_model(
            model_name=model_name,
            csv_path=CSV_PATH,
            save_path=save_path,
            learning_rate=3e-5,
            epochs=5
        )

        print("\nTraining metrics:")
        print(train_metrics)

        # Evaluate
        print("\n🔍 Evaluating on test set...")
        eval_metrics = evaluate_model(save_path, CSV_PATH)

        print("Evaluation metrics:")
        print(eval_metrics)

        # Store results
        results[model_name] = {
            "train": train_metrics,
            "eval": eval_metrics
        }

    print("📊 Final model results")

    for model, metrics in results.items():
        print(f"\nMODEL: {model}")
        print(metrics)
