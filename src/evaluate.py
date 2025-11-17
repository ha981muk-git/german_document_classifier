# evaluate.py

import torch
import numpy as np
from transformers import AutoModelForSequenceClassification
from .data_loader import load_and_prepare_data, tokenize_dataset
from typing import Dict


def evaluate_model(model_path: str, csv_path: str) -> Dict[str, float]:
    dataset, label_encoder = load_and_prepare_data(csv_path)
    dataset, tokenizer = tokenize_dataset(dataset, tokenizer_name=model_path)

    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()

    test_dataset = dataset["test"]

    logits_list = []
    labels_list = []

    for batch in test_dataset:
        inputs = {
            "input_ids": torch.tensor([batch["input_ids"]]),
            "attention_mask": torch.tensor([batch["attention_mask"]])
        }

        with torch.no_grad():
            logits = model(**inputs).logits

        logits_list.append(logits)
        labels_list.append(batch["label"])

    preds = torch.cat(logits_list).argmax(dim=1).numpy()
    labels = np.array(labels_list)

    acc = (preds == labels).mean()
    return {"accuracy": float(acc)}
