# data_loader.py
import os
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer

os.environ["WANDB_DISABLED"] = "true"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def load_and_prepare_data(csv_path, label_classes_output=None):
    df = pd.read_csv(csv_path)
    df = df[["text", "label"]].dropna()

    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["label"])

    # Only save label classes during training
    if label_classes_output is not None:
        np.save(label_classes_output, label_encoder.classes_)

    train_df, temp_df = train_test_split(
        df, test_size=0.2, stratify=df["label"], random_state=42
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.5, stratify=temp_df["label"], random_state=42
    )

    dataset = DatasetDict({
        "train": Dataset.from_dict(train_df.to_dict("list")),
        "validation": Dataset.from_dict(val_df.to_dict("list")),
        "test": Dataset.from_dict(test_df.to_dict("list"))
    })

    return dataset, label_encoder



def tokenize_dataset(dataset, tokenizer_name="dbmdz/bert-base-german-cased", max_length=512):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def tokenize(example):
        return tokenizer(
            example["text"],
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    dataset = dataset.map(tokenize, remove_columns=["text"])
    return dataset, tokenizer
