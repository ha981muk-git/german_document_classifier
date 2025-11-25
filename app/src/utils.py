# utils.py
import re
from pathlib import Path
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json

# ---------------------------
# CLEAN TEXT (shared)
# ---------------------------
def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß$€%.,\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def save_label_encoder(label_encoder: LabelEncoder, output_path: str) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, label_encoder.classes_)

def load_label_encoder(model_path: str) -> LabelEncoder:
    label_path = Path(model_path) / "label_classes.npy"
    if not label_path.exists():
        raise FileNotFoundError(f"label_classes.npy not found in {model_path}")
    classes = np.load(label_path, allow_pickle=True)
    enc = LabelEncoder()
    enc.classes_ = classes
    return enc



def save_training_config(config: dict, model_path: str) -> None:
    config_path = Path(model_path) / "training_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

