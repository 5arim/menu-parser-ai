# ocr_utils.py
from __future__ import annotations
import os, re
from typing import List
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract

# If Tesseract isn't on PATH, uncomment and set the path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def _preprocess_image(img: Image.Image) -> Image.Image:
    g = img.convert("L")
    g = ImageEnhance.Contrast(g).enhance(1.8)
    g = g.filter(ImageFilter.MedianFilter(size=3))
    g = g.filter(ImageFilter.UnsharpMask(radius=1, percent=150))
    return g

def _image_to_lines(img: Image.Image, lang: str = "eng") -> List[str]:
    cfg = r"--oem 3 --psm 6 -c preserve_interword_spaces=1"
    try:
        data = pytesseract.image_to_data(_preprocess_image(img), lang=lang, config=cfg, output_type=pytesseract.Output.DICT)
    except Exception:
        txt = pytesseract.image_to_string(_preprocess_image(img), lang=lang, config=cfg)
        return [ln.strip() for ln in txt.splitlines() if ln.strip()]

    lines = []
    current_line_num = None
    current_words = []
    for i, word in enumerate(data.get("text", [])):
        if not word or not word.strip():
            continue
        line_num = data.get("line_num", [None])[i]
        if current_line_num is None:
            current_line_num = line_num
        if line_num != current_line_num:
            if current_words:
                lines.append(" ".join(current_words))
            current_words = []
            current_line_num = line_num
        current_words.append(word)
    if current_words:
        lines.append(" ".join(current_words))
    return [re.sub(r"\s+", " ", ln).strip() for ln in lines if ln.strip()]

def extract_text(path: str, lang: str = "eng") -> str:
    path = os.path.abspath(path)
    lower = path.lower()
    gathered: List[str] = []

    if lower.endswith(".pdf"):
        from pdf2image import convert_from_path
        pages = convert_from_path(path, dpi=300)
        for page in pages:
            gathered.extend(_image_to_lines(page, lang=lang))
    else:
        img = Image.open(path)
        gathered.extend(_image_to_lines(img, lang=lang))

    out = "\n".join(line for line in gathered if line.strip())
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out
