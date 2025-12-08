import os

# Set environment variables for Hugging Face libraries before any other imports

# Unless plan to actively use Weights & Biases for experiment tracking
os.environ["WANDB_DISABLED"] = "true" # Disable Weights & Biases logging

# Can use multiple processor cores to tokenize,
# Leave it like this, Stability is more important than a minor speed-up in tokenization
os.environ["TOKENIZERS_PARALLELISM"] = "false" # Disable parallelism in tokenizers to avoid warnings and potential issues
import json
import time
import shutil
import optuna
import pandas as pd
from src.train import train_model
from pathlib import Path
from core.paths import PROJECT_ROOT, PROCESSED_DIR
import yaml

CSV_PATH = PROCESSED_DIR / "all_data.csv"

# ================================
# TOP-N CLEANUP (now top-level)
# ================================
def cleanup_folders(study, model_root, keep_top_n=2):
    """Delete all but top-N trial folders."""
    df = pd.DataFrame([
        {"trial": t.number, "value": t.value}
        for t in study.trials if t.value is not None
    ])

    if df.empty:
        return

    top = df.sort_values("value", ascending=False).head(keep_top_n)["trial"].tolist()

    # Delete all except the top-N trials
    for t in df["trial"]:
        if t not in top:
            folder = os.path.join(model_root, f"trial_{t}")
            if os.path.exists(folder):
                shutil.rmtree(folder)



# ================================
# OBJECTIVE (now clean)
# ================================
def build_objective(model_name: str, config: dict):

    model_root = str(Path("models") / model_name.replace('/', '_') / "hpo")
    hpo_config = config["hpo_config"]
    search_space = hpo_config["search_space"]

    def objective(trial):

        params = {}
        for param, settings in search_space.items():
            suggest_type = settings["type"]
            suggest_args = settings["args"]
            
            if suggest_type == "float":
                is_log = suggest_args[2] if len(suggest_args) > 2 else False
                params[param] = trial.suggest_float(param, suggest_args[0], suggest_args[1], log=is_log)
            elif suggest_type == "categorical":
                params[param] = trial.suggest_categorical(param, suggest_args[0])
            elif suggest_type == "int":
                params[param] = trial.suggest_int(param, suggest_args[0], suggest_args[1])

        trial_dir = os.path.join(model_root, f"trial_{trial.number}")
        os.makedirs(trial_dir, exist_ok=True)

        metrics = train_model(
            model_name=model_name,
            csv_path=str(CSV_PATH),
            save_path=trial_dir,
            learning_rate=params["learning_rate"],
            train_batch=params.get("batch_size"),
            eval_batch=params.get("batch_size"),
            epochs=hpo_config.get("epochs", 3),
            weight_decay=params["weight_decay"],
            dropout=params["dropout"]
        )

        trial.set_user_attr("metrics", metrics)
        return metrics["eval_f1"]

    return objective



# ================================
# RUN HPO (clean + safe)
# ================================
if __name__ == "__main__":
    # Load configuration from YAML
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    hpo_config = config["hpo_config"]
    models_to_train = config["models_to_train"]

    print(f"🚀 Starting MULTI-MODEL Optuna HPO (keep top {hpo_config['keep_top_n_trials']} trials)...")
    global_best_rows = []

    for model_name in models_to_train:

        print(f"\n🔍 Running HPO for model: {model_name}")

        model_root = str(PROJECT_ROOT / "models" / model_name.replace('/', '_') / "hpo")
        os.makedirs(model_root, exist_ok=True)

        study_name = f"hpo_{model_name.replace('/', '_')}"

        # Ensure storage path is absolute
        storage_path = hpo_config["storage_db"]
        if storage_path.startswith("sqlite:///"):
            db_file = storage_path.replace("sqlite:///", "")
            storage_path = f"sqlite:///{PROJECT_ROOT / db_file}"

        study = optuna.create_study(
            storage=storage_path,
            study_name=study_name,
            direction="maximize",
            load_if_exists=True # Allow resuming studies
        )

        objective = build_objective(model_name, config)
        study.optimize(objective, n_trials=hpo_config["n_trials"])

        # ============================
        # SAFE CLEANUP (simple & clean)
        # ============================
        cleanup_folders(study, model_root, keep_top_n=hpo_config["keep_top_n_trials"])

        # Save best hyperparameters
        best_params_path = os.path.join(model_root, "best_hyperparams.json")
        with open(best_params_path, "w") as f:
            json.dump(study.best_trial.params, f, indent=4)

        # Collect trials for CSV
        rows = []
        for t in study.trials:
            m = t.user_attrs.get("metrics", {})
            rows.append({
                "model": model_name,
                "trial": t.number,
                "eval_f1": t.value,
                **t.params,
                **m
            })

        df = pd.DataFrame(rows)
        csv_path = os.path.join(model_root, "hpo_results.csv")
        df.to_csv(csv_path, index=False)
        print(f"📄 Saved CSV: {csv_path}")

        best_n = df.sort_values("eval_f1", ascending=False).head(hpo_config["keep_top_n_trials"])

        best_trials_path = os.path.join(model_root, "best_trials.json")
        best_n.to_json(best_trials_path, orient="records", indent=4)
        print(f"🏆 Saved top-{hpo_config['keep_top_n_trials']} trials JSON: {best_trials_path}")

        global_best_rows.append(best_n)

    leaderboard = pd.concat(global_best_rows, ignore_index=True)
    leaderboard_path = hpo_config["leaderboard_path"]
    leaderboard.to_csv(leaderboard_path, index=False)

    print(f"\n📊 Global leaderboard saved at: {leaderboard_path}")
    print("\n🎉 All HPO finished successfully!")
