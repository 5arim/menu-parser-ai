# Menu Parser (OCR + Structure)

A practical pipeline to extract text from **scanned menu images** or **PDFs**, then structure it into sections with `(item, price)` pairs.

## Quick Start

1. **Install system deps**
   - **Tesseract OCR** (Windows builds: UB Mannheim)
   - **(PDFs only)** `poppler` for `pdf2image` (Windows users: install Poppler and add `bin` to PATH).

2. **Install Python deps**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Windows) Point pytesseract to tesseract.exe**  
   Either add the Tesseract folder to PATH, or set env var `TESSERACT_CMD`, e.g.:
   ```powershell
   setx TESSERACT_CMD "C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
   ```
   (Or edit `menu_parser.py` to set `pytesseract.pytesseract.tesseract_cmd` directly.)

4. **Run**
   ```bash
   python menu_parser.py path\to\menu.jpg --out result.json --csv result.csv --print
   ```

## How it works

- **PDFs**: Try embedded text via PyMuPDF. If too little text, rasterize pages with `pdf2image` and OCR each page.
- **Images**: Pillow-based preprocessing (grayscale, contrast, denoise, sharpen) → Tesseract OCR.
- **Parsing**: Heuristics detect section headers (ALL CAPS, keywords, colons). Regex captures `item + price` patterns.
- **Output**: JSON `{section: [{item, price, notes?}]}` and optional CSV.

## Tips for Accuracy

- Use `--lang eng+urd` etc. if menus include multiple languages.
- Provide higher DPI for PDFs by editing `pdf_to_text(..., dpi=300)`.
- Expand `SECTION_KEYWORDS` and `ITEM_PRICE_REGEXES` for your locales.
- If your menus are highly stylized or multi-column, consider layout analysis tools like `layoutparser` or transformer-based document parsers.

## Streamlit (optional)

You can wrap this in a simple UI:
```python
# streamlit_app.py
import json, streamlit as st
from menu_parser import process_path

st.title("Menu OCR & Parser")
f = st.file_uploader("Upload image or PDF", type=["pdf","png","jpg","jpeg","webp"])
if f:
    tmp = f.name
    with open(tmp, "wb") as out:
        out.write(f.read())
    data = process_path(tmp, lang=st.text_input("Lang", "eng"))
    st.json(data)
```

## License
MIT
