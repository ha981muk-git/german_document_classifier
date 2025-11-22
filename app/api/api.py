from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from app.src.predict import DocumentClassifier
import uuid
import os
import mimetypes
from pathlib import Path
from app.core.path import PROJECT_ROOT, APP_DIR


app = FastAPI()

# --- ENABLE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Static folder
STATIC_DIR = APP_DIR / "static"
  
# Serve static frontend
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def read_index():
    return FileResponse(STATIC_DIR / "index.html")

# Load models 

# Load available models automatically
MODEL_DIR = PROJECT_ROOT / "models"

def get_available_models():
    return [d.name for d in MODEL_DIR.iterdir() if d.is_dir()]

# Model path
DEFAULT_MODEL = PROJECT_ROOT / "models" / "deepset_gbert-base"

# Cache for loaded models
CLASSIFIERS = {}

def get_classifier(model_name: str):
    if model_name not in CLASSIFIERS:
        model_path = MODEL_DIR / model_name
        CLASSIFIERS[model_name] = DocumentClassifier(str(model_path))
    return CLASSIFIERS[model_name]



# Model from kaggle download for testing
#model_path = Path("/Users/harsh/Downloads/kaggle/working/german_document_classifier/flow_models/bert-base-german-cased")
#classifier = DocumentClassifier(str(DEFAULT_MODEL))


@app.get("/models")
async def list_models():
    return {
        "default": DEFAULT_MODEL,
        "models": get_available_models()
    }


@app.post("/predict")
async def predict(
    model_name: str = Form(DEFAULT_MODEL),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):  
    classifier = get_classifier(model_name)
    # -----------------------
    # CASE 1 — File uploaded
    # -----------------------
    if file:
        # Save temporarily
        temp_name = f"temp_{uuid.uuid4()}_{file.filename}"
        with open(temp_name, "wb") as f:
            f.write(await file.read())

        try:
            # Use universal extractor
            result = classifier.predict_file(temp_name)
        except ValueError as e:
            os.remove(temp_name)
            return {"error": str(e)}
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

        mime_type, _ = mimetypes.guess_type(file.filename)

        return {
            "mode": "file",
            "filename": file.filename,
            "mime_type": mime_type,
            "result": result
        }

    # -----------------------
    # CASE 2 — Raw text
    # -----------------------
    if text:
        result = classifier.predict(text)
        return {"mode": "text", "result": result}

    # -----------------------
    # CASE 3 — Nothing provided
    # -----------------------
    return {"error": "Provide text or upload a file"}
