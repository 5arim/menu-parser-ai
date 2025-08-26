
# Menu Parser (OCR + Structured Output)

An **AI-assisted pipeline** to extract text from **scanned restaurant menus (images or PDFs)** and structure it into clean sections with `(item, price, notes)` pairs.

---

## ✨ Features

* **OCR Support**
  Works with **images** (`.jpg`, `.png`, `.webp`) and **PDFs** (text-based or scanned).
* **Text Cleaning**
  Grayscale, denoise, contrast boost, and sharpening improve OCR accuracy.
* **Menu Parsing**
  Automatically detects **sections** (e.g., *Starters*, *Drinks*, *Desserts*) and extracts `item + price` pairs.
* **Flexible Outputs**
  Save structured data into **JSON** or **CSV**.
* **Optional LLM Integration**
  Designed to optionally connect with a **local model** (e.g., *Mistral-4Q GGUF*) or **cloud LLMs** (Gemini, OpenAI, Claude) for more **accurate structuring**.

  > ⚠️ LLM integration is currently disabled by default (due to large size). You can enable it later.

---

## 🚀 Quick Start

### 1. Install system dependencies

* **Tesseract OCR** → [Download (UB Mannheim build)](https://github.com/UB-Mannheim/tesseract/wiki)
* **Poppler (for PDFs)** → [Windows download](https://blog.alivate.com.au/poppler-windows/)

👉 Add Poppler’s `bin/` folder to your **PATH**.

---

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Tesseract (Windows only)

Either add it to **PATH** or manually set `TESSERACT_CMD`:

```powershell
setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Or in `menu_parser.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\...\tesseract.exe"
```

---

### 4. Run parser

```bash
python menu_parser.py path\to\menu.jpg --out result.json --csv result.csv --print
```

---

## ⚙️ How It Works

1. **PDF Handling**

   * Extract text with PyMuPDF.
   * If empty → rasterize pages with `pdf2image` → OCR.

2. **Image Handling**

   * Preprocessing with Pillow → OCR via Tesseract.

3. **Parsing**

   * Regex + heuristics detect **section headers** and `item + price` lines.
   * Outputs structured dictionary:

     ```json
     {
       "Starters": [
         {"item": "Spring Rolls", "price": "$5.99", "notes": ""}
       ]
     }
     ```

4. **Outputs**

   * JSON → programmatic use
   * CSV → spreadsheets

---

## 🎯 Tips for Better Accuracy

* For multi-language menus:

  ```bash
  python menu_parser.py menu.jpg --lang eng+urd
  ```
* For PDFs → increase DPI (`dpi=300`) in `pdf_to_text`.
* Customize regex & keywords in `parse_rules.py`.
* For **multi-column menus**, try `layoutparser` or transformer-based parsers.

---

## 🌐 Optional Streamlit UI

```bash
streamlit run streamlit_app.py
```

Upload a menu file → see structured JSON instantly.

---

## 🤖 LLM Integration (Optional)

* **Local Models**
  *Mistral-4Q* (GGUF format, via `llama.cpp` or `ctransformers`).

* **Cloud Models**
  Works with **Gemini**, **OpenAI GPT**, or **Claude** for smarter structuring.

LLMs can:
✔ Fix OCR typos
✔ Merge split lines
✔ Improve category grouping

> Default repo runs **without LLMs** to stay lightweight.
> You can plug in LLM support later if needed.

---

## 📌 Roadmap

* [ ] Smarter multi-column parsing
* [ ] Better multilingual OCR
* [ ] Plug-and-play LLM adapters
* [ ] Drag-and-drop **web upload** + REST API

---

## 🤝 Contributing

PRs, regex improvements, and new parsing rules are welcome!

---

## 📜 License

MIT

---
