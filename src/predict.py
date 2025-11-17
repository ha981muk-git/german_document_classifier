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
            page_text = page.get_text()

            if page_text.strip():
                text += page_text
            else:
                # OCR fallback for scanned pages
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes()))
                text += pytesseract.image_to_string(img, lang="deu")

        return text

    # -----------------------
    # EXTRACT TEXT FROM IMAGE (OCR)
    # -----------------------
    def extract_text_from_image(self, image_path):
        img = Image.open(image_path)
        try:
            return pytesseract.image_to_string(img, lang="deu")
        except:
            return pytesseract.image_to_string(img)  # English fallback


    # -----------------------
    # EXTRACT TEXT FROM DOCX
    # -----------------------
    def extract_text_from_docx(self, docx_path):
        document = docx.Document(docx_path)
        return "\n".join([p.text for p in document.paragraphs])

    # -----------------------
    # UNIVERSAL EXTRACTOR
    # Handles PDF, image, text, docx
    # -----------------------
    def extract_text_from_any(self, file_path):
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
    def predict_file(self, file_path):
        extracted_text = self.extract_text_from_any(file_path)
        return self.predict(extracted_text)

    # -----------------------
    # PREDICT TEXT DIRECTLY
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
