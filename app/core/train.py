
import torch, os,json

from pathlib import Path
from typing import Any, Dict, Optional

from sklearn.metrics import precision_recall_fscore_support
from transformers import EarlyStoppingCallback
from transformers import AutoModelForSequenceClassification, AutoConfig, TrainingArguments, Trainer, DataCollatorWithPadding

from app.core.data_loader import load_and_prepare_data, tokenize_dataset
from app.core.utils import save_training_config
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

def get_sensible_batch_sizes(device, user_train_batch=None, user_eval_batch=None, user_gradient_accumulation=None):
    """
    Selects sensible default batch sizes and FP16 settings based on the device
    if the user has not provided them.
    """
    if user_train_batch is None:
        if device.type == "cuda":
            return 4, 8, 2, True
        elif device.type == "mps":
            return 4, 4, 2, False
        else:
            return 2, 4, 4, False
    else:
        fp16 = (device.type == "cuda")
        eval_batch = user_eval_batch or (user_train_batch * 2)
        gradient_acc = user_gradient_accumulation or 1
        return user_train_batch, eval_batch, gradient_acc, fp16



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
    gradient_accumulation: Optional[int] = None,  
    dropout: Optional[float] = None,
    early_stopping_patience: int = 3,  
    data_split_config: Optional[Dict] = None,
)-> Dict[str, Any]:

    print(f"📌 Using device: {device}")

    # Adaptive batch size based on device
    # If user did NOT provide batch sizes, auto-adjust safely
    # Adaptive batch size based on device
    # Then in train_model():
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)

    # ===== GET OPTIMAL BATCH SIZES & FP16 SETTING =====
    train_batch_size, eval_batch_size, grad_accum, use_fp16 = get_sensible_batch_sizes(
        device,
        user_train_batch=train_batch,
        user_eval_batch=eval_batch,
        user_gradient_accumulation=gradient_accumulation
    )

    data_split_config = data_split_config or {}
    dataset, label_encoder = load_and_prepare_data(
        csv_path,
        label_classes_output=f"{save_path}/label_classes.npy",
        **data_split_config
    )

    dataset, tokenizer = tokenize_dataset(dataset, tokenizer_name=model_name, batch_size=1000)

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
        output_dir=str(save_path),
        num_train_epochs=epochs,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_steps=warmup_steps,

        per_device_train_batch_size=train_batch_size, 
        per_device_eval_batch_size=eval_batch_size,    
        gradient_accumulation_steps=grad_accum,  

        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        logging_steps=50,

        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,

        fp16=use_fp16,
        #gradient_checkpointing=(device.type == "cuda"),
        gradient_checkpointing=True,
        report_to="none",
        dataloader_pin_memory=(device.type != "mps"),# Disable pin_memory on Mac (MPS) to stop the warning
    )

    early_stopping = EarlyStoppingCallback(
    early_stopping_patience=early_stopping_patience,
    early_stopping_threshold=0.0
    )

    # Data collator for dynamic padding
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        callbacks=[early_stopping],
    )

    # The train() method returns the final training metrics
    train_result = trainer.train()

    # The best model is already loaded thanks to `load_best_model_at_end=True`
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

    # Save training configuration
    # To get training accuracy (if computed during training), we often look at state.log_history
    global_train_metrics = train_result.metrics

    # Capture the best validation metrics from the training process
    print("Verifying best model on validation set...")
    best_val_metrics = trainer.evaluate(eval_dataset=dataset["validation"])

    # Now, explicitly evaluate on the held-out test set
    print("Evaluating on the final test set...")
    test_metrics = trainer.evaluate(eval_dataset=dataset["test"])
    print(f"Test metrics: {test_metrics}")

        # Helper to get dataset counts safely
    def get_count(split_name):
        return len(dataset[split_name]) if split_name in dataset else 0

    # --- UNIFIED REPORT STRUCTURE ---
    experiment_report = {
        "experiment_id": f"EXP-{model_name}-{os.urandom(2).hex()}",
        "model_type": model_name,
        
        # 1. THE RECIPE (Formerly 'training_config')
        "hyperparameters": {
            "learning_rate": learning_rate,
            "epochs": epochs,
            "train_batch_size": train_batch_size,
            "eval_batch_size": eval_batch_size,
            "gradient_accumulation_steps": grad_accum,
            "weight_decay": weight_decay,
            "warmup_steps": warmup_steps,
            "dropout": dropout,
            "device": str(device),
            "fp16_enabled": use_fp16
        },

        # 2. THE DATASET INFO
        "dataset_config": {
            "num_labels": len(label_encoder.classes_),
            "label_classes": label_encoder.classes_.tolist(),
            "splitting_strategy": {
                "training_count": get_count("train"),
                "validation_count": get_count("validation"),
                "test_count": get_count("test")
            }
        },

        # 3. THE PHASES (Train -> Val -> Test)
        "phases": {
            "1_training": {
                "status": "completed",
                "metrics": {
                    "final_training_loss": global_train_metrics.get("train_loss"),
                    "total_runtime_seconds": global_train_metrics.get("train_runtime")
                }
            },
            "2_validation": {
                "purpose": "Model Selection",
                "metrics": {
                    "validation_loss": best_val_metrics.get("eval_loss"),
                    "validation_f1": best_val_metrics.get("eval_f1"),
                    "validation_accuracy": best_val_metrics.get("eval_accuracy")
                }
            },
            "3_testing": {
                "purpose": "Real-world Simulation",
                "metrics": {
                    "test_loss": test_metrics.get("eval_loss"),
                    "test_accuracy": test_metrics.get("eval_accuracy"),
                    "test_f1": test_metrics.get("eval_f1"),
                    "test_precision": test_metrics.get("eval_precision"),
                    "test_recall": test_metrics.get("eval_recall")
                }
            }
        },

        # 4. GENERAL EVALUATION SUMMARY
        "general_evaluation": {
            "summary": "Combined performance metrics and configuration.",
            "deployment_decision": "APPROVED" if test_metrics.get("eval_f1", 0) > 0.8 else "NEEDS_REVIEW"
        }
    }

    
    save_training_config(experiment_report, str(save_path))

    return {
        "validation": best_val_metrics,
        "test": test_metrics
    }

    """
    Deefault return block: --- IGNORE --
    trainer.train()

    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

    # Evaluate on test set and return metrics
    return trainer.evaluate(eval_dataset=dataset["test"])
    # also work for default 
    # return trainer.evaluate()
    """