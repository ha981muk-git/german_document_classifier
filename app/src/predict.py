from pathlib import Path
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import re
import io
import mimetypes
import docx  # for DOCX files
from typing import Dict, Any
from pathlib import Path
from .utils import load_label_encoder
from app.core.path import APP_DIR

# Device detection
device = (
    torch.device("cuda") if torch.cuda.is_available() else
    torch.device("mps") if torch.backends.mps.is_available() else
    torch.device("cpu")
)

# Get APP_DIR (one level up from src/)
PREDICTION_MODEL = APP_DIR / "models" / "dbmdz_bert-base-german-cased"


class DocumentClassifier:
    def __init__(self, model_path:str = PREDICTION_MODEL)-> None:
        # Load tokenizer + model
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)   # <-- move model to device
        self.model.eval()

        # Load label classes for ID → Label mapping
        self.label_encoder = load_label_encoder(model_path)
        self.label_classes = self.label_encoder.classes_

    # -----------------------
    # CLEAN TEXT (preprocessing)
    # -----------------------
    def preprocess_text(self, text: str) -> str:
        text = text.replace("\n", " ")
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß$€%.,\s-]", " ", text)
        return text.lower().strip()

    def page_contains_image(self, page):
        """Detect whether a PDF page contains image blocks (PyMuPDF type 1)."""
        try:
            info = page.get_text("dict")
        except:
            return False

        blocks = info.get("blocks", [])
        if not blocks:
            return False

        for block in blocks:
            # PyMuPDF image blocks have type == 1
            if block.get("type") == 1:
                return True

        return False


    # -----------------------
    # EXTRACT TEXT FROM PDF
    # -----------------------
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        # FIX 4) use context manager to avoid resource leaks
        with fitz.open(pdf_path) as doc:
            for page in doc:

                # If page contains images → OCR fallback
                if self.page_contains_image(page):
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    text += pytesseract.image_to_string(img, lang="deu")
                    continue

                # If page has real selectable text
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
                else:
                    # No detectable text → fallback OCR
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    text += pytesseract.image_to_string(img, lang="deu")
        return text

    # -----------------------
    # EXTRACT TEXT FROM IMAGE (OCR)
    # -----------------------
    def extract_text_from_image(self, image_path: str) -> str:
        img = Image.open(image_path)
        try:
            return pytesseract.image_to_string(img, lang="deu")
        except:
            return pytesseract.image_to_string(img)  


    # -----------------------
    # EXTRACT TEXT FROM DOCX
    # -----------------------
    def extract_text_from_docx(self, docx_path: str) -> str:
        document = docx.Document(docx_path)
        return "\n".join([p.text for p in document.paragraphs])

    # -----------------------
    # UNIVERSAL EXTRACTOR
    # Handles PDF, image, text, docx
    # -----------------------
    def extract_text_from_any(self, file_path: str)  -> str:
        mime, _ = mimetypes.guess_type(file_path)

        if mime is None:
            raise ValueError("Unknown file type")

        # --- PDF ---
        if mime == "application/pdf":
            return self.extract_text_from_pdf(file_path)

        # --- IMAGES ---
        if mime.startswith("image/"):
            return self.extract_text_from_image(file_path)

        # --- TEXT FILES ---
        if mime.startswith("text/"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        # --- DOCX ---
        if mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self.extract_text_from_docx(file_path)

        # --- Add more file types here ---
        raise ValueError(f"Unsupported file type: {mime}")

    # -----------------------
    # UNIVERSAL FILE PREDICT
    # -----------------------
    def predict_file(self, file_path: str) -> Dict[str, Any]:
        extracted_text = self.extract_text_from_any(file_path)
        return self.predict(extracted_text)

    # -----------------------
    # PREDICT TEXT DIRECTLY
    # -----------------------
    def predict(self, text: str) -> Dict[str, Any]:
        clean = self.preprocess_text(text)

        inputs = self.tokenizer(
            clean,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        pred_id = int(probs.argmax())
        confidence = float(probs[pred_id])

        # pred_id = logits.argmax(dim=-1).cpu().numpy()[0]
        label = self.label_classes[pred_id]

        return {
            "label": str(label),
            "label_id": pred_id,
            "confidence": confidence
        }