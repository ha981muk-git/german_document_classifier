import os
import json
import optuna
import pandas as pd
from src.train import train_model

CSV_PATH = "./data/data_processed/all_data.csv"

MODELS = [
    "deepset/gbert-base",
    "dbmdz/bert-base-german-cased",
]



# ------------------------------
# Objective function for Optuna
# ------------------------------
def build_objective(model_name):

    def objective(trial):

        # Search space
        lr = trial.suggest_float("learning_rate", 1e-6, 5e-5, log=True)
        dropout = trial.suggest_float("dropout", 0.0, 0.3)
        weight_decay = trial.suggest_float("weight_decay", 0.0, 0.3)
        batch_size = trial.suggest_categorical("batch_size", [2, 4, 8])


        model_dir = f"./models/{model_name.replace('/', '_')}/hpo/trial_{trial.number}"
        os.makedirs(model_dir, exist_ok=True)

        metrics = train_model(
            model_name=model_name,
            csv_path=CSV_PATH,
            save_path=model_dir,
            learning_rate=lr,
            train_batch=batch_size,
            eval_batch=batch_size,
            epochs=3,
            weight_decay=weight_decay,
            dropout=dropout
        )

        # store metrics so Optuna can export later
        trial.set_user_attr("metrics", metrics)

        return metrics["f1"]

    return objective


# ------------------------------
# Run HPO for all models
# ------------------------------
if __name__ == "__main__":
    print("🚀 Starting MULTI-MODEL Optuna HPO...")

    global_best_rows = []  # For final leaderboard CSV

    for model_name in MODELS:

        
        print(f"🔍 Running HPO for model: {model_name}")


        # Model-specific directory
        base_dir = f"./models/{model_name.replace('/', '_')}/hpo"
        os.makedirs(base_dir, exist_ok=True)

        # Study persistence DB
        study_path = os.path.join(base_dir, "study.db")
        study = optuna.create_study(
            direction="maximize",
            study_name=f"hpo_{model_name.replace('/', '_')}",
            storage=f"sqlite:///{study_path}",
            load_if_exists=True,
            pruner=optuna.pruners.MedianPruner(),
            sampler=optuna.samplers.TPESampler(seed=42)  # safer and deterministic
        )


        objective = build_objective(model_name)

        # Run optimization
        study.optimize(objective, n_trials=10)

        # -------------------------------
        # Save best hyperparameters JSON
        # -------------------------------
        best_params_path = os.path.join(base_dir, "best_hyperparams.json")
        with open(best_params_path, "w") as f:
            json.dump(study.best_trial.params, f, indent=4)

        # -------------------------------
        # Save ALL trial results to CSV
        # -------------------------------
        rows = []
        for t in study.trials:
            m = t.user_attrs.get("metrics", {})
            rows.append({
                "model": model_name,
                "trial": t.number,
                "f1": t.value,
                **t.params,
                **m  # accuracy, recall, etc.
            })

        df = pd.DataFrame(rows)
        csv_path = os.path.join(base_dir, "hpo_results.csv")
        df.to_csv(csv_path, index=False)

        print(f"📄 Saved CSV with all trials: {csv_path}")

        # -------------------------------
        # Save top 5 best trials JSON
        # -------------------------------
        trials_sorted = df.sort_values("f1", ascending=False)
        best_5 = trials_sorted.head(5)

        best_trials_path = os.path.join(base_dir, "best_trials.json")
        best_5.to_json(best_trials_path, orient="records", indent=4)

        print(f"🏆 Saved top 5 best trials JSON: {best_trials_path}")

        # Add top 5 to global leaderboard
        global_best_rows.append(best_5)

    # -------------------------------
    # Save GLOBAL leaderboard CSV
    # -------------------------------
    if global_best_rows:
        leaderboard = pd.concat(global_best_rows, ignore_index=True)

    leaderboard_path = "./models/hpo_leaderboard.csv"
    leaderboard.to_csv(leaderboard_path, index=False)

    print(f"\n📊 Global leaderboard saved at: {leaderboard_path}")
    print("\n🎉 ALL HPO FINISHED SUCCESSFULLY!")
