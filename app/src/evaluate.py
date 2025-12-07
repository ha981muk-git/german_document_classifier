# evaluate.py

import torch
import numpy as np
from transformers import AutoModelForSequenceClassification
from .data_loader import load_and_prepare_data, tokenize_dataset
from typing import Dict, Optional
from transformers import AutoTokenizer
from torch.utils.data import DataLoader
from sklearn.metrics import precision_recall_fscore_support

# Device detection
device = (
    torch.device("cuda") if torch.cuda.is_available() else
    torch.device("mps") if torch.backends.mps.is_available() else
    torch.device("cpu")
)

def evaluate_model(
    model_path: str, csv_path: str, data_split_config: Optional[Dict] = None
) -> Dict[str, float]:
    # 1. Load data
    data_split_config = data_split_config or {}
    dataset, _ = load_and_prepare_data(csv_path, **data_split_config)

    # 2. Load tokenizer correctly
    dataset, _ = tokenize_dataset(dataset, tokenizer_name=str(model_path))
    dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    # 3. Load model and set device
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()

    # 4. Batch loader
    test_loader = DataLoader(dataset["test"], batch_size=32) # Larger batch size for eval is fine

    all_preds = []
    all_labels = []

    # 5. Iterate batches
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        with torch.no_grad():
            logits = model(input_ids=input_ids, attention_mask=attention_mask).logits

        preds = logits.argmax(dim=1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # Calculate comprehensive metrics
    p, r, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average="weighted", zero_division=0
    )
    accuracy = (all_preds == all_labels).mean()

    return {
        "accuracy": float(accuracy),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
    }