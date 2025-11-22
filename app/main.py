# main.py
import sys

from src.train import train_model
from src.evaluate import evaluate_model
from pathlib import Path
from core.path import APP_DIR, PROJECT_ROOT

MODELS = [
    "deepset/gbert-base",
#    "dbmdz/bert-base-german-cased",
]

CSV_PATH = APP_DIR / "data" / "data_processed" / "all_data.csv"


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
            epochs=1
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
