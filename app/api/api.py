import uuid
import tempfile
import shutil
import mimetypes
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.paths import PROJECT_ROOT, APP_DIR
from app.core.predict import DocumentClassifier


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

def get_available_models() -> list[str]:
    return [d.name for d in MODEL_DIR.iterdir() if d.is_dir()]

AVAILABLE_MODELS = get_available_models()
DEFAULT_MODEL_NAME = "deepset_gbert-base" if "deepset_gbert-base" in AVAILABLE_MODELS else (AVAILABLE_MODELS[0] if AVAILABLE_MODELS else None)

# Cache for loaded models
CLASSIFIERS = {}

def get_classifier(model_name: str):
    if model_name not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' not found. Available models: {AVAILABLE_MODELS}"
        )

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
        "default_model": DEFAULT_MODEL_NAME,
        "available_models": AVAILABLE_MODELS
    }


@app.post("/predict")
async def predict(
    model_name: str = Form(DEFAULT_MODEL_NAME),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):  
    if not model_name:
        raise HTTPException(status_code=400, detail="No models available to process request.")

    classifier = get_classifier(model_name)
    # -----------------------
    # CASE 1 — File uploaded
    # -----------------------
    if file:
        # Use a secure temporary directory
        temp_dir = tempfile.mkdtemp()
        try:
            temp_name = Path(temp_dir) / file.filename
            with open(temp_name, "wb") as f:
                shutil.copyfileobj(file.file, f)
            result = classifier.predict_file(temp_name)
        finally:
            shutil.rmtree(temp_dir) # Clean up the directory and its contents

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
    raise HTTPException(status_code=400, detail="Provide 'text' or upload a 'file'.")
