from email import generator
import sys
from pathlib import Path
import yaml
import pandas as pd
from collections import defaultdict

from core.paths import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR
from sampler.make_synthetic_data import SyntheticDocumentGenerator
from src.prepare_data import process_dataset
from src.train import train_model
from sampler.doc_generator import save_all_synthetic_as_text_files
from src.evaluate import evaluate_model
import json
import argparse
from datetime import datetime


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
    """Optional dataset preparation (commented out in your current version)."""

    raw_csv = Path(PROCESSED_DIR) / "raw_data.csv"
    process_dataset(RAW_DIR, str(raw_csv), config["label_map"])

    if SYNTHETIC_DIR is not None:
        synthetic_csv = Path(PROCESSED_DIR) / "synthetic_data.csv"
        process_dataset(SYNTHETIC_DIR, str(synthetic_csv), config["label_map"])


# -----------------------------
# Main Training Loop
# -----------------------------

def main() -> None:

    # Load configuration from YAML
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    parser = argparse.ArgumentParser(description="German Document Classifier Pipeline")
    parser.add_argument("--generate", action="store_true", help="Step 1: Generate synthetic data files.")
    parser.add_argument("--prepare", action="store_true", help="Step 2: Prepare datasets from raw/synthetic files into CSVs.")
    parser.add_argument("--train", action="store_true", help="Step 3: Train models on the prepared data.")
    parser.add_argument("--all", action="store_true", help="Run the full pipeline (generate, prepare, and train).")
    args = parser.parse_args()

    if args.generate or args.all:
        print("GENERATING SYNTHETIC DATA V0 ...")
        save_all_synthetic_as_text_files(
            per_category=config["synthetic_data"]["per_category_v0"],
            output_dir=str(SYNTHETIC_DIR),
            overwrite=config["synthetic_data"]["overwrite"]
        )
        print("GENERATING SYNTHETIC DATA V1 ...")
        generator = SyntheticDocumentGenerator(per_category=config["synthetic_data"]["per_category_v1"], output_dir=str(SYNTHETIC_DIR))
        generator.generate_documents(overwrite=config["synthetic_data"]["overwrite"])

    if args.prepare or args.all:
        print("PREPARING DATASETS")
        prepare_datasets(config)

    if args.train or args.all:
        print("TRAINING MODELS")
        processed_dir = Path(PROCESSED_DIR)
        csv_path = combine_csv_files(processed_dir)

        results = defaultdict(dict)

        for model_name in config["models_to_train"]:
            print(f"\n🚀 Training {model_name}")

            save_path = str(PROJECT_ROOT / "models" / model_name.replace("/", "_"))

            # train_model now returns the final test metrics after evaluating the best model
            all_metrics = train_model(
                model_name=model_name,
                csv_path=str(csv_path),
                save_path=save_path,
                learning_rate=config["training"]["learning_rate"],
                epochs=config["training"]["epochs"],
                data_split_config=config.get("data_split", {})
            )
            results[model_name] = all_metrics

        print("\n📊 Final model results summary:")
        for model, metrics in results.items():
            print(f"\n--- MODEL: {model} ---")
            print("  Validation Metrics:", metrics.get("validation", "N/A"))
            print("  Test Metrics:", metrics.get("test", "N/A"))
            print("--------------------" + "-" * len(model))

        # Save the final results to a JSON file with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"evaluation_results_{timestamp}.json"
        results_path = PROJECT_ROOT / "models" / results_filename
        print(f"\n💾 Saving final results to {results_path}")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()
