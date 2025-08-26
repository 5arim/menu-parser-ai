# menu_parser.py
from __future__ import annotations
import json
from typing import Dict, List, Optional, Any
from ocr_utils import extract_text
from parse_rules import rule_based_parse
from llm_extractor import llm_structured_extract

def process_path(path: str, lang: str = "eng", use_llm: bool = True) -> Dict[str, List[Dict[str, Optional[str]]]]:
    raw = extract_text(path, lang=lang) or ""
    # Write debug OCR output (inspect if empty or junk)
    try:
        with open("debug_ocr_output.txt", "w", encoding="utf-8") as f:
            f.write(raw)
    except Exception:
        pass

    if not raw.strip():
        return {}

    if use_llm:
        try:
            out = llm_structured_extract(raw)
            if out:
                return out
        except Exception as e:
            print(f"[menu_parser] LLM parse failed: {e}")

    return rule_based_parse(raw)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python menu_parser.py <path>")
        raise SystemExit(2)
    print(json.dumps(process_path(sys.argv[1]), ensure_ascii=False, indent=2))
