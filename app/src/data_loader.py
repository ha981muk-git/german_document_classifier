# data_loader.py
import os
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer
from typing import Optional, Tuple
from transformers import PreTrainedTokenizer

from .utils import save_label_encoder

os.environ["WANDB_DISABLED"] = "true"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def load_and_prepare_data(csv_path: str,
                          label_classes_output: Optional[str]=None,
                          validation_test_split_size: float = 0.3,
                          test_proportion_of_split: float = 0.5,
                          random_state: int = 42
    ) -> Tuple[DatasetDict, LabelEncoder]:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    
    required_columns = {"text", "label"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # CLEAN NANs
    df = df[["text", "label"]].dropna()

    # Prevent Data Leakage by removing duplicates
    df = df.drop_duplicates(subset=["text"])

    # Prevent crash in train_test_split if a class has only 1 item
    df = df.groupby('label').filter(lambda x: len(x) >= 3)

    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["label"])

    # Only save label classes during training
    if label_classes_output is not None:
        save_label_encoder(label_encoder, label_classes_output)

    train_df, temp_df = train_test_split(
        df, test_size=validation_test_split_size, stratify=df["label"], random_state=random_state
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=test_proportion_of_split, stratify=temp_df["label"], random_state=random_state
    )

    dataset = DatasetDict({
        "train": Dataset.from_dict(train_df.to_dict("list")),
        "validation": Dataset.from_dict(val_df.to_dict("list")),
        "test": Dataset.from_dict(test_df.to_dict("list"))
    })

    return dataset, label_encoder



def tokenize_dataset(dataset:DatasetDict, tokenizer_name: str ="dbmdz/bert-base-german-cased", max_length: int = 512,batch_size: int = 1000) -> Tuple[DatasetDict, PreTrainedTokenizer]:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def tokenize(example):
        return tokenizer(
            example["text"],
            truncation=True,
            max_length=max_length
        )

    dataset = dataset.map(
        tokenize,
        batched=True,
        batch_size=batch_size,
        remove_columns=[col for col in dataset["train"].column_names if col != "label"],
    )


    return dataset, tokenizer
