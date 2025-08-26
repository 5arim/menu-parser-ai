# streamlit_app.py
from __future__ import annotations
import json, os, uuid, streamlit as st
from typing import Dict, List, Optional
from menu_parser import process_path

st.set_page_config(page_title="Menu OCR + Local Mistral Parser", layout="wide")
st.title("📄 Menu OCR ➜ Local Mistral (GGUF) ➜ Editable Menu")

st.write("Upload a scanned menu (image or PDF). The app will OCR it, parse via your local Mistral GGUF model (served by llm_server.py), then let you edit and download JSON.")

with st.sidebar:
    st.header("Settings")
    use_llm = st.checkbox("Use local LLM parser (requires llm_server.py running)", value=True)
    lang = st.text_input("Tesseract languages", value="eng")
    st.caption("Examples: 'eng' or 'eng+urd' if you installed extra languages in Tesseract.")

uploaded = st.file_uploader("Drop your menu (PDF or image)", type=["pdf","png","jpg","jpeg","webp","tif","tiff"])

if uploaded:
    suffix = os.path.splitext(uploaded.name)[1] or ".bin"
    tmp_path = f"_upload_{uuid.uuid4().hex}{suffix}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.read())

    st.info("⏳ Running OCR + parsing (may take some seconds)...")
    data = process_path(tmp_path, lang=lang, use_llm=use_llm)

    try:
        os.remove(tmp_path)
    except Exception:
        pass

    if not data:
        st.error("❌ No items found. Inspect debug_ocr_output.txt to see raw OCR output.")
    else:
        st.success("✅ Parsed! Review & edit below:")
        if "menu_data" not in st.session_state:
            st.session_state.menu_data = data

        new_data: Dict[str, List[Dict[str, Optional[str]]]] = {}
        for section, items in st.session_state.menu_data.items():
            with st.expander(f"📂 {section}", expanded=True):
                new_section_name = st.text_input("Section name", value=section, key=f"sec_{section}")
                updated_items: List[Dict[str, Optional[str]]] = []
                for i, row in enumerate(items):
                    cols = st.columns([3,2,3,1])
                    with cols[0]:
                        item = st.text_input("Item", value=row.get("item",""), key=f"{section}_item_{i}")
                    with cols[1]:
                        price = st.text_input("Price", value=row.get("price",""), key=f"{section}_price_{i}")
                    with cols[2]:
                        notes = st.text_input("Notes", value=row.get("notes",""), key=f"{section}_notes_{i}")
                    with cols[3]:
                        remove = st.checkbox("Remove", key=f"{section}_rm_{i}")
                    if not remove:
                        updated_items.append({"item": item, "price": price, "notes": notes})
                if st.button(f"➕ Add item to '{new_section_name}'"):
                    updated_items.append({"item":"", "price":"", "notes":""})
                new_data[new_section_name] = updated_items

        st.session_state.menu_data = new_data
        st.download_button("📥 Download JSON", data=json.dumps(st.session_state.menu_data, ensure_ascii=False, indent=2), file_name="menu_clean.json", mime="application/json")
