# utils.py
import json
import fitz  # PyMuPDF
import sys
import pytesseract
import io
import re

import pillow_heif
pillow_heif.register_heif_opener()

from PIL import Image
from pathlib import Path
import numpy as np
from sklearn.preprocessing import LabelEncoder


# ---------------------------
# CLEAN TEXT (shared)
# ---------------------------
def clean_text(text: str) -> str:
    #  Normalize Newlines/HTML (Standard cleaning)
    text = text.replace("\n", " ")
    text = re.sub(r"<[^>]+>", " ", text)

    #  REMOVE FORM NOISE (Crucial Step)
    
    # Pattern A: Matches long sequences of dots or underscores (e.g., ".......", "_______")
    # We replace them with a single space
    text = re.sub(r'[._-]{2,}', ' ', text)
    
    # Pattern B: Matches "spaced out" lines often found in OCR forms (e.g., "_ _ _ _ _")
    # This looks for an underscore followed by whitespace, repeated 2 or more times
    text = re.sub(r'(?:_\s){2,}_?', ' ', text)

    #  Filter allowed characters
    # Note: We keep '.' in the allowed list for sentence endings, 
    # but since ran Step 2, the long "....." lines are already gone
    text = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß$€%.,\s-]", " ", text)

    # 4. Collapse multiple spaces and trim
    text = re.sub(r"\s+", " ", text)
    
    return text.lower().strip()

# -----------------------
# EXTRACT TEXT FROM PDF
# -----------------------


def extract_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF.
    Priority:
    1. Direct text extraction (fast, accurate).
    2. OCR fallback if the page is a scanned image (slow).
    """
    full_text = ""
    
    def _page_contains_image(page) -> bool:
        """Detect whether a PDF page contains image blocks (PyMuPDF type 1)."""
        try:
            info = page.get_text("dict")
        except:
            return False
        blocks = info.get("blocks", [])
        if not blocks:
            return False
        for block in blocks:
            if block.get("type") == 1:
                return True
        return False

    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                # 1. Try to get digital text first
                page_text = page.get_text()
                
                if page_text.strip(): # If meaningful digital text exists, use it
                    full_text += page_text
                
                # 2. If no digital text, check if it's a scanned image and then use OCR
                elif _page_contains_image(page):
                    # Render page as an image
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    img = img.convert("RGB") # Ensure compatibility with pytesseract
                    # Perform OCR (assuming German based on your previous context)
                    ocr_text = pytesseract.image_to_string(img, lang='deu')
                    full_text += ocr_text

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}", file=sys.stderr)

    return full_text


def save_label_encoder(label_encoder: LabelEncoder, output_path: str) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, label_encoder.classes_)

def load_label_encoder(model_path: str) -> LabelEncoder:
    label_path = Path(model_path) / "label_classes.npy"
    if not label_path.exists():
        raise FileNotFoundError(f"label_classes.npy not found in {model_path}")
    classes = np.load(label_path, allow_pickle=True)
    enc = LabelEncoder()
    enc.classes_ = classes
    return enc



def save_training_config(config: dict, model_path: str) -> None:
    config_path = Path(model_path) / "experiment_report.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
