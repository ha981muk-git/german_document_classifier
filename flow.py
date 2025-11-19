from metaflow import FlowSpec, step, Parameter
import sys
from src.train import train_model  
from pathlib import Path


GERMAN_MODELS = [
    "dbmdz/bert-base-german-cased",
    "bert-base-german-cased",   
    "deepset/gbert-base"
]



class GermanModelFlow(FlowSpec):

    csv_path = Parameter(
        "csv",
        default="./data/data_processed/all_data.csv"
    )

    @step
    def start(self):
        print("🚀 Starting Metaflow multi-model pipeline")



        self.model_list = GERMAN_MODELS
        self.next(self.train_each_model, foreach="model_list")

    @step
    def train_each_model(self):
        model_name = self.input
        print(f"Training: {model_name}")

        
        save_path = Path("flow_models") / model_name.replace('/', '_')
        save_path.mkdir(parents=True, exist_ok=True)

        save_path = str(save_path)  # convert to string after creating folder


        self.metrics = train_model(
            model_name=model_name,
            csv_path=self.csv_path,
            save_path=save_path,
            epochs=5,
            learning_rate=3e-5
        )

        self.model_name = model_name
        self.next(self.join)

    @step
    def join(self, inputs):
        print("📊 Aggregating results")

        self.results = {i.model_name: i.metrics for i in inputs}

        for name, metrics in self.results.items():
            print(f"\n{name}: {metrics}")

        self.next(self.end)

    @step
    def end(self):
        print("🎉 Pipeline finished!")
        print("All results:", self.results)


if __name__ == "__main__":
    GermanModelFlow()
