# **📘 German Document Classifier**


This document provides a structure for developers working on the **German Document Classifier**.

*   **Included:** Installation steps, project structure, and usage instructions.
*   **Deep Dive:** For architecture and technical details, please see the [Technical System Documentation](./APPENDIX.md).


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
uvicorn app.api.api:app --reload --port 8080
```

Send free‑form text for classification:
```bash
curl -X POST http://127.0.0.1:8080/predict \
     -F "model_name=bert-base-german-cased" \
     -F "text=Dies ist eine deutsche Beispielrechnung."
```

Send pdf for classification:
```bash
curl -X POST http://127.0.0.1:8080/predict \
     -F "model_name=bert-base-german-cased" \
     -F "file=@app/data/raw/contracts/01_Vertrag.pdf"
```
### Open the UI:
👉 http://localhost:8080

## **2.8 🐳 Running with Docker (Alternative)**

For easier dependency management and deployment, you can build and run the entire application using Docker. This is the recommended way to run the service in production. But you need to train and get the model first for testing the model.

### **Build the Docker Image**

```bash
docker build -t german-document-classifier .
```

### **Run the Docker Container**
```bash
docker run -p 8080:8080 german-document-classifier
```
### Allows:

1. **✔ Uploading PDFs, images:** `classifier.predict_file` extracts text via OCR/loader logic before inference.
2. **✔ Text classification:** Directly send German text via the form field or curl request.
3. **✔ Real-time inference:** The model is loaded once at startup, keeping latency low for repeated predictions.



### **2.9 Hyperparameter Searching**

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
