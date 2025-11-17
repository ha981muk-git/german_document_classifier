# predict.py

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import re
import io

DEFAULT_MODEL = "../models/dbmdz_bert-base-german-cased"

class DocumentClassifier:
    def __init__(self, model_path=DEFAULT_MODEL):
        # Load tokenizer + model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

        # Load label classes for ID → Label mapping
        self.label_classes = np.load(f"{model_path}/label_classes.npy", allow_pickle=True)

    # -----------------------
    # CLEAN TEXT (preprocessing)
    # -----------------------
    def preprocess_text(self, text):
        text = text.replace("\n", " ")
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s$€%.,-]", " ", text)
        return text.lower().strip()

    # -----------------------
    # EXTRACT TEXT FROM PDF
    # -----------------------
    def extract_text_from_pdf(self, pdf_path):
        text = ""
        doc = fitz.open(pdf_path)

        for page in doc:
            # Extract text normally
            page_text = page.get_text()

            if page_text.strip():
                text += page_text
            else:
                # OCR fallback if page has no text layer
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes()))

                text += pytesseract.image_to_string(img, lang="deu")

        return text

    # -----------------------
    # PREDICT TEXT
    # -----------------------
    def predict(self, text):
        clean = self.preprocess_text(text)

        inputs = self.tokenizer(
            clean,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits

        pred_id = logits.argmax(dim=-1).cpu().numpy()[0]
        label = self.label_classes[pred_id]

        return {
            "label": str(label),
            "label_id": int(pred_id)
        }

    # -----------------------
    # PREDICT PDF
    # -----------------------
    def predict_pdf(self, pdf_path):
        extracted = self.extract_text_from_pdf(pdf_path)
        return self.predict(extracted)
