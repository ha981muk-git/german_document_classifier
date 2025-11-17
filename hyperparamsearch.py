import os
import json
import time
import shutil
import optuna
import pandas as pd
from src.train import train_model

CSV_PATH = "./data/data_processed/all_data.csv"
STORAGE_URL = "sqlite:///optuna_studies.db"

MODELS = [
    "deepset/gbert-base",
    "dbmdz/bert-base-german-cased"
]

# ------------------------------
# Objective function for Optuna
# ------------------------------
def build_objective(model_name, keep_top_n=2):

    model_root = f"./models/{model_name.replace('/', '_')}/hpo"

    def cleanup_folders(study):
        """Delete all but top-N trials folders."""
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

    def objective(trial):

        # Search space
        lr = trial.suggest_float("learning_rate", 1e-6, 5e-5, log=True)
        dropout = trial.suggest_float("dropout", 0.0, 0.3)
        weight_decay = trial.suggest_float("weight_decay", 0.0, 0.3)
        batch_size = trial.suggest_categorical("batch_size", [2, 4, 8])

        trial_dir = os.path.join(model_root, f"trial_{trial.number}")
        os.makedirs(trial_dir, exist_ok=True)

        metrics = train_model(
            model_name=model_name,
            csv_path=CSV_PATH,
            save_path=trial_dir,
            learning_rate=lr,
            train_batch=batch_size,
            eval_batch=batch_size,
            epochs=3,
            weight_decay=weight_decay,
            dropout=dropout
        )

        trial.set_user_attr("metrics", metrics)

        # Clean up after each trial
        cleanup_folders(trial.study)

        return metrics["eval_f1"]

    return objective


# ------------------------------
# Run HPO for all models
# ------------------------------
if __name__ == "__main__":
    print("🚀 Starting MULTI-MODEL Optuna HPO (Top-2 memory-saving mode)...")

    global_best_rows = []

    for model_name in MODELS:

        print(f"\n🔍 Running HPO for model: {model_name}")

        base_dir = f"./models/{model_name.replace('/', '_')}/hpo"
        os.makedirs(base_dir, exist_ok=True)

        study_name = f"hpo_{model_name.replace('/', '_')}_{int(time.time())}"

        study = optuna.create_study(
            storage=STORAGE_URL,
            study_name=study_name,
            direction="maximize",
            load_if_exists=False
        )

        objective = build_objective(model_name)
        study.optimize(objective, n_trials=10)

        # Save best hyperparameters
        best_params_path = os.path.join(base_dir, "best_hyperparams.json")
        with open(best_params_path, "w") as f:
            json.dump(study.best_trial.params, f, indent=4)

        # Save summary of top-2 trials
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
        csv_path = os.path.join(base_dir, "hpo_results.csv")
        df.to_csv(csv_path, index=False)

        print(f"📄 Saved CSV: {csv_path}")

        # Only keep top-2
        best_n = df.sort_values("eval_f1", ascending=False).head(2)

        best_trials_path = os.path.join(base_dir, "best_trials.json")
        best_n.to_json(best_trials_path, orient="records", indent=4)

        print(f"🏆 Saved top-2 trials JSON: {best_trials_path}")

        global_best_rows.append(best_n)

    # Global leaderboard
    leaderboard = pd.concat(global_best_rows, ignore_index=True)
    leaderboard_path = "./models/hpo_leaderboard.csv"
    leaderboard.to_csv(leaderboard_path, index=False)

    print(f"\n📊 Global leaderboard saved at: {leaderboard_path}")
    print("\n🎉 All HPO finished successfully!")
