from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from src.predict import DocumentClassifier
import uuid
import os
import mimetypes


app = FastAPI()

# --- ENABLE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


# Load model once
classifier = DocumentClassifier("./models/dbmdz_bert-base-german-cased")


@app.post("/predict")
async def predict(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
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
