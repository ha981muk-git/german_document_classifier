
---

# **📘 Developer Documentation**

This document provides a clean, professional structure for developers working on the **German Document Classifier** project.
All installation steps, architecture explanations, and usage instructions from the original text are preserved and reorganized.


---

# **0.0 🚀 Getting Started**



# **1.0 Running in Google Colab / Kaggle**

### **Clone the Repository**

Run the following commands in a Colab/Kaggle cell to clone the project and navigate into the directory:

```bash
!git clone https://github.com/ha981muk-git/german_document_classifier.git
%cd german_document_classifier
```

### **Install Dependencies**

```bash
!pip install uv
!uv pip install --system -r pyproject.toml
```



### **Fine-Tune the BERT Model**

Execute the main script to start the fine-tuning process:

```bash
!python -m app.main --train
```

# **2.0 🛠️ Installation ( Local Development)**
## **Prerequisites**

### **Before Cloning the Repository**



Ensure you have **uv** installed.
```bash
# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
---
## **2.1 Clone the repository**

```bash
git clone https://github.com/ha981muk-git/german_document_classifier.git
cd german_document_classifier
```

## **2.2 Create virtual environment**

```bash
uv sync

# MacOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```
---


### **2.3 Synthetic Data Generation (Optional)**

```bash
python -m  app.main --generate
```

### **2.4 Prepare CSV File  For Datasets Training (Optional)**

```bash
python -m app.main --prepare
```

## **2.5 Training the BERT Models**

```bash
python -m app.main --train
```

## **2.6 Alternatively Generate, Prepare and Training the BERT Models (All At Once)**

```bash
python -m app.main --all
```

## **2.7 FastAPI Web Server**

The FastAPI service wraps the trained `DocumentClassifier` and exposes a single `/predict` endpoint that powers both the web UI and any programmatic client. It accepts either a `text` form field (for raw strings) or a `file` upload (for PDFs, images, or DOCs) and routes the request to the right inference path. Because the server also mounts the static frontend under `/`, you only need one process to serve both the UI and the API.

Start the server :
```bash
uvicorn app.api.api:app --reload --port 8000
```

Send free‑form text for classification:
```bash
curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Dies ist eine deutsche Beispielrechnung."
```

Send pdf for classification:
```bash
curl -X POST http://127.0.0.1:8000/predict \
     -F "file=@app/data/data_raw/contracts/01_Vertrag.pdf;type=application/pdf"
```
### Open the UI:
👉 http://localhost:8000

### Allows:

1. **✔ Uploading PDFs, images:** `classifier.predict_file` extracts text via OCR/loader logic before inference.
2. **✔ Text classification:** Directly send German text via the form field or curl request.
3. **✔ Real-time inference:** The model is loaded once at startup, keeping latency low for repeated predictions.



### **2.8 Hyperparameter Searching**

```bash
python -m app.hyperparamsearch
```

## **3. 📁 Project Structure**

```text
german_document_classifier/
│
├── config.yaml
├── environment.yaml
├── requirements.txt
├── optuna_studies.db
│
├── app/
│   ├── main.py
│   ├── flow.py
│   ├── hyperparamsearch.py
│   │
│   ├── api/
│   │   └── api.py
│   │
│   ├── core/
│   │   ├── evaluate.py
│   │   ├── paths.py
│   │   ├── prepare_data.py
│   │   ├── predict.py
│   │   └── train.py
│   │
│   ├── data/
│   │   └── (data files not shown)
│   │
│   ├── sampler/
│   │   ├── doc_generator.py
│   │   └── make_synthetic_data.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   └── style.css
│   │
│   └── notebooks/
│       ├── 01_data_exploration.ipynb
│       ├── 02_model_training.ipynb
│       ├── 03_evaluation.ipynb
│       ├── 04_data_extraction.ipynb
│       ├── colab.ipynb
│       └── kaggle.ipynb
│
└── README.md

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

**Module:** `app/core/prepare_data.py`

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

**Module:** `app/core/train.py`

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

**Module:** `app/core/evaluate.py`

The evaluation pipeline:

* Reloads model, tokenizer, and label encoder
* Recreates tokenized dataset for consistency
* Computes accuracy and class-level metrics
* Aggregates metrics into a structured dictionary
* Ensures reproducible test results (fixed random seed)

---

## **A.6 Hyperparameter Optimization**

**Module:** `app/hyperparamsearch.py`

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

**Module:** `app/flow.py`

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

**Module:** `app/core/predict.py`

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

**Module:** `app/api/api.py`

The web service exposes the following endpoints:

* `POST /predict`

  * Accepts text or file uploads
  * Executes the complete inference pipeline
  * Returns JSON with label and confidence
* `GET /`

  * Serves the frontend interface
* `app/static/*`

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