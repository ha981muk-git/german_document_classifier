from typing import Dict, Optional
import torch, os
from transformers import AutoModelForSequenceClassification, AutoConfig, TrainingArguments, Trainer
from .data_loader import load_and_prepare_data, tokenize_dataset
from sklearn.metrics import precision_recall_fscore_support

# Device detection
device = (
    torch.device("cuda") if torch.cuda.is_available() else
    torch.device("mps") if torch.backends.mps.is_available() else
    torch.device("cpu")
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(-1)
    p, r, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted", zero_division=0
    )
    acc = (preds == labels).mean()
    
    return {
        "accuracy": float(acc),
        "precision": float(p),
        "recall": float(r),
        "f1": float(f1),
    }



def train_model(
    model_name: str,
    csv_path: str,
    save_path: str,
    learning_rate: float = 3e-5,
    epochs: int = 1,
    train_batch: int = None,  
    eval_batch: int = None,   
    weight_decay: float = 0.0,
    warmup_steps: int = 0,
    gradient_accumulation: int = None,  
    dropout: float = None,
)-> Dict[str, float]:

    print(f"📌 Using device: {device}")

    # Adaptive batch size based on device
    # If user did NOT provide batch sizes, auto-adjust safely
    # Adaptive batch size based on device
    if train_batch is None:
        if device.type == "cuda":
            fp16 = True
            train_batch = 4
            eval_batch = eval_batch or 8
            gradient_accumulation = gradient_accumulation or 2
        elif device.type == "mps":
            fp16 = False
            train_batch = 4
            eval_batch = eval_batch or 8
            gradient_accumulation = gradient_accumulation or 2
        else:  # CPU
            fp16 = False
            train_batch = 2
            eval_batch = eval_batch or 4
            gradient_accumulation = gradient_accumulation or 4
    else:
        # User provided batch sizes
        fp16 = (device.type == "cuda")
        eval_batch = eval_batch or train_batch * 2  # Default eval batch to 2x train
        gradient_accumulation = gradient_accumulation or 1


    os.makedirs(save_path, exist_ok=True)

    dataset, label_encoder = load_and_prepare_data(
        csv_path,
        label_classes_output=f"{save_path}/label_classes.npy"
    )

    dataset, tokenizer = tokenize_dataset(dataset, tokenizer_name=model_name)

    # Load model
    if dropout is None:
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(label_encoder.classes_),
            ignore_mismatched_sizes=True
        ).to(device)
    else:
        config = AutoConfig.from_pretrained(model_name)
        config.num_labels = len(label_encoder.classes_)
        config.hidden_dropout_prob = dropout
        config.attention_probs_dropout_prob = dropout
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            config=config,  # ← Pass config here
            ignore_mismatched_sizes=True
        ).to(device)


    # TrainingArguments
    args = TrainingArguments(
        output_dir=save_path,
        num_train_epochs=epochs,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_steps=warmup_steps,

        per_device_train_batch_size=train_batch, 
        per_device_eval_batch_size=eval_batch,    
        gradient_accumulation_steps=gradient_accumulation,  

        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        logging_steps=50,

        fp16=fp16,
        gradient_checkpointing=(device.type == "cuda"),
        report_to="none",
    )


    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        compute_metrics=compute_metrics,
    )

    trainer.train()

    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

    return trainer.evaluate()

