# baseline.py

import json
import pickle
from pathlib import Path
import pandas as pd
from typing import Dict, Any

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from app.src.utils import clean_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)

# ============================================================
# =============== TRAIN & SAVE BASELINE MODEL =================
# ============================================================

def train_tfidf_logreg(csv_path: str, save_dir: str) -> Dict[str, Any]:
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    texts = df["text"].astype(str).apply(clean_text)

    # Label encoding
    le = LabelEncoder()
    labels = le.fit_transform(df["label"])

    # Splits
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 3),
        min_df=2,
        sublinear_tf=True,
        stop_words="german",
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Logistic Regression
    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
        C=2.0,
    )

    clf.fit(X_train_vec, y_train)
    preds = clf.predict(X_test_vec)

    # Metrics
    acc = accuracy_score(y_test, preds)
    p, r, f1, _ = precision_recall_fscore_support(
        y_test, preds, average="weighted", zero_division=0
    )

    # ---------------------------
    # SAVE MODEL COMPONENTS
    # ---------------------------

    # vectorizer
    with open(save_dir / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    # classifier
    with open(save_dir / "classifier.pkl", "wb") as f:
        pickle.dump(clf, f)

    # label classes
    import numpy as np
    np.save(save_dir / "label_classes.npy", le.classes_)

    # config
    config = {
        "max_features": 50000,
        "ngram_range": (1, 3),
        "min_df": 2,
        "sublinear_tf": True,
        "stop_words": "german",
        "model_type": "tfidf+logreg"
    }
    with open(save_dir / "config.json", "w") as f:
        json.dump(config, f, indent=4)

    return {
        "accuracy": float(acc),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
        "save_path": str(save_dir)
    }


# ============================================================
# ====================== LOAD & PREDICT ======================
# ============================================================

class TfidfLogRegModel:
    def __init__(self, model_dir: str):
        model_dir = Path(model_dir)

        # load vectorizer
        with open(model_dir / "vectorizer.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)

        # load classifier
        with open(model_dir / "classifier.pkl", "rb") as f:
            self.clf = pickle.load(f)

        # load label encoder
        import numpy as np
        classes = np.load(model_dir / "label_classes.npy", allow_pickle=True)
        self.label_classes = classes

    def preprocess(self, text: str) -> str:
        return clean_text(text)

    def predict(self, text: str) -> Dict[str, Any]:
        clean = self.preprocess(text)
        vec = self.vectorizer.transform([clean])
        probs = self.clf.predict_proba(vec)[0]
        pred_id = probs.argmax()
        label = self.label_classes[pred_id]

        return {
            "label": str(label),
            "label_id": int(pred_id),
            "confidence": float(probs[pred_id])
        }


"""
from baseline import train_tfidf_logreg

metrics = train_tfidf_logreg(
    csv_path="data/train.csv",
    save_dir="models/baseline_tfidf"
)

print(metrics)


"""

"""

from baseline import TfidfLogRegModel

model = TfidfLogRegModel("models/baseline_tfidf")
prediction = model.predict("Dies ist ein Testtext für die Klassifikation.")
print(prediction)


"""