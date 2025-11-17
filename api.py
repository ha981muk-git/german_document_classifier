# api.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from src.predict import DocumentClassifier


app = FastAPI()

# Load classifier once at startup
classifier = DocumentClassifier("./models/deepset_gbert-base")  # Adjust path as needed


# ----------------------------
# Request model for text input
# ----------------------------
class DocumentRequest(BaseModel):
    text: str


# ----------------------------
# 1) TEXT CLASSIFICATION
# ----------------------------
@app.post("/predict-text")
def classify_text(request: DocumentRequest):
    result = classifier.predict(request.text)
    return {"result": result}


# ----------------------------
# 2) PDF CLASSIFICATION
# ----------------------------
@app.post("/predict-pdf")
async def classify_pdf(file: UploadFile = File(...)):
    # Save the uploaded PDF temporarily
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = classifier.predict_pdf(temp_path)
    return {"result": result}
