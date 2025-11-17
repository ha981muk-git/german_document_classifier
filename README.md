
---

# **📘 Developer Documentation**

This document provides a clean, professional structure for developers working on the **German Document Classifier** project.
All installation steps, architecture explanations, and usage instructions from the original text are preserved and reorganized.

---

# **1. 🚀 Getting Started**

## **1.1 Running in Google Colab (Recommended)**

If the project is stored in Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```

After mounting, your project will appear under:

```
/content/drive/MyDrive/PATH_TO_PROJECT/german_document_classifier/
```

### **Install dependencies**

```bash
!pip install -r "/content/drive/MyDrive/PATH_TO_PROJECT/german_document_classifier/requirements.txt"
```

### **Change to the project folder**

```bash
%cd /content/drive/MyDrive/PATH_TO_PROJECT/german_document_classifier/
```

### **Fine-Tune BERT MODEL**

```bash
!python /content/drive/MyDrive/PATH_TO_PROJECT/german_document_classifier/main.py
```

---

# **2. 🛠️ Installation (Local Development)**

## **2.1 Clone the repository**

```bash
git clone https://github.com/ha981muk-git/german_document_classifier.git
cd german_document_classifier
```

## **2.2 Create virtual environment**

```bash
conda env create -f environment.yaml
conda activate doc-classifier-env
```
---


### **2.3 Synthetic Data Generation**

```bash
python tests/doc_generator.py
```
## **2.4 Training the BERT Models**

```bash
python main.py
```
## **2.5 FastAPI Web Server**



Start the server:
```bash
uvicorn api:app --reload --port 8000
```



### Open the UI:
👉 http://localhost:8000

### Allows:

1. **✔ Uploading PDFs, images**
2. **✔ Text classification**
3. **✔ Real-time inference**

# **3. 📁 Project Structure**

### **2.6 Hyperparameter Searching**

```bash
python hyperparamsearch.py
```
## **2.4 Training the BERT Models**


```text
german_document_classifier/
│
├── src/
│   ├── train.py              # Model training (HuggingFace Trainer)
│   ├── evaluate.py           # Evaluation pipeline
│   ├── data_loader.py        # Data loading, preprocessing, tokenization
│   ├── predict.py            # DocumentClassifier (OCR + inference logic)
│   ├── utils.py              # Utility and helper functions
│
├── notebooks/                # jupyternotebook for various purpose
├── models/                   # Saved models, tokenizers, configs
├── static/                   # Frontend files (served by FastAPI)
│   ├── index.html            # html page
│   ├── style.css
├── data/                     # Raw and processed datasets (CSV)
│
├── environment.yaml          # packages and dependencies   
├── main.py                   # Training + evaluation entry script
├── hyperparamsearch.py       # Optuna hyperparameter optimization
├── flow.py                   # Automated multi-model training pipeline
├── api.py                    # FastAPI backend (file upload + prediction)
│
└── README.md                 # Project documentation
```


# **📎 Appendix A — Technical System Documentation**

## **A.1 Overview of the System**

The system developed in project implements a complete, modular pipeline for **automated document classification** using multiple German BERT-based models.
The architecture covers all major components of a contemporary machine learning workflow:

1. **Data preprocessing and tokenization**
2. **Fine-tuning and evaluation of Transformer-based language models**
3. **Hyperparameter optimization (HPO)**
4. **Workflow automation using Metaflow**
5. **OCR-based document ingestion and preprocessing**
6. **A unified inference engine for various document types**
7. **A FastAPI-based web service for real-time predictions**

The system supports both *text-based documents* and *image-based or scanned documents* (e.g., PDF scans).
All architectural elements are designed to be reproducible, configurable, and extensible for research purposes.

---



---
## **A.2 System Architecture**

The overall architecture consists of several loosely coupled and independently testable modules.
Figure A.1 provides a high-level representation of the data and processing flow:

```
+------------------------------------------------------------+
|                     FastAPI Web Interface                  |
+-------------------------+----------------------------------+
                          |
                          v
+------------------------------------------------------------+
|                     Inference Layer                        |
|   (OCR → Preprocessing → Tokenization → BERT Model → CLS)  |
+------------------------------------------------------------+
                          |
                          v
+------------------------------------------------------------+
|                 Training & Evaluation Layer                |
| (HF Trainer, metrics, dropout, batch schedules, early stop)|
+------------------------------------------------------------+
                          |
                          v
+------------------------------------------------------------+
|                   Hyperparameter Optimization              |
|                       (Optuna Search)                      |
+------------------------------------------------------------+
                          |
                          v
+------------------------------------------------------------+
|               Workflow Orchestration (Metaflow)            |
+------------------------------------------------------------+
                          |
                          v
+------------------------------------------------------------+
|                     Data Layer (CSV input)                 |
+------------------------------------------------------------+
```

**Figure A.1:** High-level architectural overview of the implemented system.

Each layer exposes clearly defined interfaces and can be executed independently (training, HPO, inference, pipelines, etc.).
This separation of concerns improves the reproducibility and maintainability of the system.

---

## **A.3 Data Processing Layer**

**Module:** `src/data_loader.py`

Responsibilities:

* CSV ingestion with schema validation
* Conversion into HuggingFace `DatasetDict`
* Stratified splitting into train/validation/test sets
* Label encoding using `LabelEncoder`
* Dataset tokenization using a user-selected Transformer tokenizer
* Batch-size aware mapping for efficient preprocessing
* Removal of non-model features

This design ensures consistency between training, evaluation, and inference.

---

## **A.4 Model Training Layer**

**Module:** `src/train.py`

The training subsystem implements:

* Automatic device detection (CUDA/MPS/CPU)
* Dynamic batch size selection based on available hardware
* Mixed-precision training (FP16 when supported)
* Configurable dropout, weight decay, warmup steps
* Gradient accumulation for memory-constrained environments
* Early stopping
* Best-model checkpointing
* Unified metric computation (accuracy, precision, recall, F1)

All training parameters are stored in a `training_config.json` file to ensure full experiment reproducibility.

---

## **A.5 Evaluation Layer**

**Module:** `src/evaluate.py`

The evaluation pipeline:

* Reloads model, tokenizer, and label encoder
* Recreates tokenized dataset for consistency
* Computes accuracy and class-level metrics
* Aggregates metrics into a structured dictionary
* Ensures reproducible test results (fixed random seed)

---

## **A.6 Hyperparameter Optimization**

**Module:** `hyperparamsearch.py`

Hyperparameter optimization is based on **Optuna**.
The implementation includes:

* Search spaces for:

  * learning rate
  * dropout
  * weight decay
  * batch size
* Trial directories for experiment isolation
* Automatic cleanup policy (retain top-N trials only)
* Structured export of metrics to:

  * CSV
  * JSON
* Generation of a **global HPO leaderboard** across models

This subsystem ensures efficient exploration of model configurations while minimizing disk overhead.

---

## **A.7 Workflow Automation**

**Module:** `flow.py`

The system incorporates an automated training pipeline using **Metaflow**, featuring:

* Parallel model training via `foreach` branches
* Automatic aggregation of results
* Fault isolation between models
* A reproducible end-to-end experiment workflow

Pipeline flow structure:

```
start → train_each_model (foreach) → join → end
```

---

## **A.8 Inference Layer (DocumentClassifier)**

**Module:** `src/predict.py`

The inference engine provides a unified abstraction for document classification.
It supports multiple input formats:

| File Type             | Extraction Method          |
| --------------------- | -------------------------- |
| PDF (text-based)      | PyMuPDF                    |
| PDF (scanned)         | OCR fallback via Tesseract |
| Images (JPG/PNG/TIFF) | OCR                        |
| DOCX                  | python-docx                |
| TXT                   | UTF-8 file reader          |

Processing pipeline:

1. MIME-based file type detection
2. Text extraction (PDF/OCR/DOCX/Text)
3. Tokenization
4. BERT inference
5. Softmax + label decoding

The module loads the pretrained model and the corresponding label encoder to produce final predictions with confidence scores.

---

## **A.9 FastAPI Service Layer**

**Module:** `api.py`

The web service exposes the following endpoints:

* `POST /predict`

  * Accepts text or file uploads
  * Executes the complete inference pipeline
  * Returns JSON with label and confidence
* `GET /`

  * Serves the frontend interface
* `/static/*`

  * Hosts all frontend assets

Additional features:

* CORS (Cross-Origin Resource Sharing)
* Asynchronous file handling
* Temporary storage with cleanup mechanisms

---

## **A.10 Reproducibility Considerations**

To ensure repeatable results, the system provides:

* Fixed random seeds in all data splits
* Serialization of:

  * model weights
  * tokenizer
  * label encoder (`label_classes.npy`)
  * training configuration
  * HPO outcomes
* Deterministic train/val/test partitioning
* Explicit versioning of model directories
* Device-dependent batch size logging

---

## **A.11 Summary of Technical Contributions**

The developed system integrates:

* **End-to-end ML pipeline engineering**
* **Modular and reproducible architecture**
* **Multi-model benchmarking**
* **OCR-enhanced document ingestion**
* **Real-time inference API**
* **Hyperparameter optimization and workflow automation**

This appendix provides the technical foundation for interpreting and reproducing the experimental results presented in the main chapters of the project.

---

