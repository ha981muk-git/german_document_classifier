from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from src.predict import DocumentClassifier
import uuid
import os

app = FastAPI()

# --- ENABLE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (if you have other static files, they go in the "static" directory)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html at the root
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# Load once
classifier = DocumentClassifier("models/dbmdz_bert-base-german-cased")

@app.post("/predict")
async def predict(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    # If PDF provided
    if file:
        if not file.filename.lower().endswith(".pdf"):
            return {"error": "Only PDF files allowed"}

        temp_name = f"temp_{uuid.uuid4()}.pdf"

        with open(temp_name, "wb") as f:
            f.write(await file.read())

        result = classifier.predict_pdf(temp_name)

        os.remove(temp_name)

        return {"mode": "pdf", "result": result}

    # If Text provided
    if text:
        result = classifier.predict(text)
        return {"mode": "text", "result": result}

    return {"error": "Provide either a PDF or text"}