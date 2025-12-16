import os, sys

# First app import to ensure PROJECT_ROOT is added to sys.path
from app.core.paths import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, SYNTHETIC_DIR

# Set environment variables for Hugging Face libraries before any other imports

# Unless plan to actively use Weights & Biases for experiment tracking
os.environ["WANDB_DISABLED"] = "true" # Disable Weights & Biases logging

# Can use multiple processor cores to tokenize,
# Leave it like this, Stability is more important than a minor speed-up in tokenization
os.environ["TOKENIZERS_PARALLELISM"] = "false" # Disable parallelism in tokenizers to avoid warnings and potential issues


import yaml
import json
import argparse
import pandas as pd

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from app.sampler.make_synthetic_data import SyntheticDocumentGenerator 
from app.sampler.doc_generator import save_all_synthetic_as_text_files

from app.core.evaluate import evaluate_model
from app.core.prepare_data import prepare_datasets, combine_csv_files
from app.core.train import train_model
from app.statistics.result import generate_results

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
    parser.add_argument("--results", action="store_true", help="Step 4: Generate CSV and graphs of the models' results.")
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
        print("Combining CSV files into a single dataset...")
        combine_csv_files(Path(PROCESSED_DIR))

    if args.train or args.all:
        print("TRAINING MODELS")
        csv_path = Path(PROCESSED_DIR) / "all_data.csv"

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
    # write perser for results

    if args.results or args.all:
        print("Generate CSV and graphs of the models' results")
        generate_results()

if __name__ == "__main__":
    main()
