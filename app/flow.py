import os

# Set environment variables for Hugging Face libraries before any other imports

# Unless plan to actively use Weights & Biases for experiment tracking
os.environ["WANDB_DISABLED"] = "true" # Disable Weights & Biases logging

# Can use multiple processor cores to tokenize,
# Leave it like this, Stability is more important than a minor speed-up in tokenization
os.environ["TOKENIZERS_PARALLELISM"] = "false" # Disable parallelism in tokenizers to avoid warnings and potential issues

from metaflow import FlowSpec, step, Parameter
from src.train import train_model  
from pathlib import Path
from core.paths import PROJECT_ROOT, PROCESSED_DIR
import yaml

class GermanModelFlow(FlowSpec):

    csv_path = Parameter(
        "csv",
        help="Path to the training data CSV file.",
        default=str(PROCESSED_DIR / "all_data.csv")
    )

    # Parameters can now override the config file
    epochs = Parameter("epochs", help="Number of training epochs.", default=None, type=int)
    learning_rate = Parameter("lr", help="Learning rate.", default=None, type=float)

    @step
    def start(self):
        print("🚀 Starting Metaflow multi-model pipeline")
        
        # Load configuration from YAML
        config_path = PROJECT_ROOT / "config.yaml"
        print(f"Loading configuration from: {config_path}")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Use models defined in the config file
        self.model_list = self.config["models_to_train"]
        print(f"Models to train: {self.model_list}")

        self.next(self.train_each_model, foreach="model_list")

    @step
    def train_each_model(self):
        self.model_name = self.input
        print(f"\n--- Training: {self.model_name} ---")

        # Define a unique path for this model run
        save_path = str(PROJECT_ROOT / "flow_models" / self.model_name.replace("/", "_"))
        self.save_path = save_path

        # Get training params from config, but allow overrides from CLI Parameters
        training_config = self.config["training"]
        lr = self.learning_rate if self.learning_rate is not None else training_config["learning_rate"]
        num_epochs = self.epochs if self.epochs is not None else training_config["epochs"]

        # train_model returns a dict with 'validation' and 'test' keys
        all_metrics = train_model(
            model_name=self.model_name,
            csv_path=self.csv_path,
            save_path=save_path,
            learning_rate=lr,
            epochs=num_epochs,
            data_split_config=self.config.get("data_split", {})
        )

        # Extract the key test metrics to pass to the join step
        test_metrics = all_metrics.get("test", {})
        self.test_f1 = test_metrics.get("eval_f1", 0.0)
        self.test_accuracy = test_metrics.get("eval_accuracy", 0.0)

        self.next(self.join)

    @step
    def join(self, inputs):
        print("📊 Aggregating results")

        # Create a leaderboard of model performance from all parallel runs
        leaderboard = [
            {
                "model_name": i.model_name,
                "test_f1": i.test_f1,
                "test_accuracy": i.test_accuracy,
                "saved_path": i.save_path,
            }
            for i in inputs
        ]

        # Sort by F1 score to find the best model
        self.leaderboard = sorted(leaderboard, key=lambda x: x["test_f1"], reverse=True)
        self.best_model = self.leaderboard[0] if self.leaderboard else None

        self.next(self.end)
    @step
    def end(self):
        print("🎉 Pipeline finished!")
        print("\n--- FINAL LEADERBOARD (sorted by F1 score) ---")
        for result in self.leaderboard:
            print(f"  - Model: {result['model_name']}, F1: {result['test_f1']:.4f}, Accuracy: {result['test_accuracy']:.4f}")
        
        if self.best_model:
            print(f"\n🏆 Best performing model: {self.best_model['model_name']}")
            print(f"   - Saved at: {self.best_model['saved_path']}")

if __name__ == "__main__":
    GermanModelFlow()
