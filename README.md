

---

# Menu Parser (OCR + Structured Output)

An AI-assisted pipeline to extract text from **scanned restaurant menus (images or PDFs)** and structure it into clean sections with `(item, price, notes)` pairs.

---

## ✨ Features

* **OCR Support**
  Works with images (`.jpg`, `.png`, `.webp`) and PDFs (text-based or scanned).
* **Text Cleaning**
  Preprocessing steps (grayscale, contrast, denoise, sharpen) improve OCR accuracy.
* **Menu Parsing**
  Detects categories/sections (e.g., *Drinks*, *Starters*, *Desserts*) and captures `item + price` pairs.
* **Output Formats**
  Save results to **JSON** or **CSV** for downstream use.
* **Optional LLM Integration**
  Designed to work with a local or external LLM (e.g., Mistral-4Q in GGUF format) for **better structured parsing**.

  > ⚠️ Currently, the LLM model is disabled in this repo because of heavy size. You can plug it back in when needed.

---

## 🚀 Quick Start

### 1. Install system dependencies

* **Tesseract OCR** ([Windows builds: UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki))
* **(PDF only)** [Poppler](https://blog.alivate.com.au/poppler-windows/) for `pdf2image`

  > Add Poppler’s `bin/` folder to your PATH

---

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Tesseract (Windows only)

Add Tesseract to your PATH or set `TESSERACT_CMD` manually:

```powershell
setx TESSERACT_CMD "C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

Alternatively, edit `menu_parser.py` to set:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\...\tesseract.exe"
```

---

### 4. Run parser

```bash
python menu_parser.py path\to\menu.jpg --out result.json --csv result.csv --print
```

---

## ⚙️ How it works

1. **PDF Handling**

   * Extract text via PyMuPDF.
   * If empty/low text → convert each page to image (`pdf2image`) → OCR.

2. **Image Handling**

   * Pillow preprocessing → OCR with Tesseract.

3. **Parsing**

   * Detect section headers (ALL CAPS, keywords, colons).
   * Regex for item + price extraction.
   * Group results into `{section: [{item, price, notes}]}`

4. **Outputs**

   * JSON for programmatic use
   * CSV for spreadsheets

---

## 🎯 Tips for Better Accuracy

* Multi-language menus → `--lang eng+urd`
* PDFs → increase DPI (`dpi=300`) for sharper text.
* Expand `parse_rules.py` with **section keywords** and **price regexes** tuned for your locale.
* For highly styled or multi-column menus → try `layoutparser` or deep-learning models like `Donut` / `LayoutLM`.

---

## 🌐 Streamlit UI (optional)

You can run a quick web UI for testing:

```bash
streamlit run streamlit_app.py
```

![streamlit demo](https://via.placeholder.com/600x250?text=Streamlit+Menu+Parser+Demo)

---

## 🤖 LLM Integration (optional)

* **Local Model**: Mistral-4Q (GGUF format)

  * You can run via [llama.cpp](https://github.com/ggerganov/llama.cpp) or `ctransformers` in Python.
  * Used for **intelligent structuring** of OCR text.
* **Cloud Models**: Can integrate with **Gemini**, **OpenAI GPT**, or **Anthropic Claude** if desired.

> For lightweight experiments, LLM is optional — heuristic parsing already works.
> For production accuracy, LLM gives **cleaner categories, better grouping, and typo handling**.

---

## 📌 Roadmap

* [ ] Improve parsing for multi-column menus
* [ ] Enhance multilingual OCR support
* [ ] Plug-and-play LLM integration (choose local or cloud)
* [ ] Web-based drag-and-drop upload + API

---

## 🤝 Contributing

PRs are welcome! Ideas, bug reports, or regex improvements are highly appreciated.

---

## 📜 License

MIT

---


