# llm_extractor.py
from __future__ import annotations
import re, json, requests
from typing import Dict, List, Optional, Any

SYSTEM_PROMPT = """
You are a menu parser. Input is pre-processed OCR text from restaurant menus.
Your job:
- Detect sections/categories (e.g., Starters, Drinks, Main Course).
- Each category has multiple items with "item", "price", and "notes".
- Extract prices if present (numbers only). If missing, leave price as "".
- Group items under the nearest section header.
Return ONLY valid JSON with structure:
{
  "Section Name": [
    {"item":"Name", "price":"123", "notes":""},
    ...
  ],
  ...
}
Do not add extra commentary — only return valid JSON.
"""

# Default endpoint (matches llm_server.py)
DEFAULT_LLM_ENDPOINT = "http://127.0.0.1:8000/v1/chat/completions"
DEFAULT_MODEL_NAME = "mistral"  # model field is not used by server but kept for compatibility

_BADCHARS_RE = re.compile(r"[^A-Za-z0-9\s\|\-.,'()\/₹$€£:]+")

def _preprocess_for_llm(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        s = _BADCHARS_RE.sub(" ", s)
        s = re.sub(r"\s+", " ", s).strip()
        # detect price at end
        m = re.search(r"(\d{2,5}(?:[.,]\d{2})?)\s*$", s)
        if m:
            price = m.group(1)
            s = s[:m.start()].strip()
            lines.append(f"{s} | {price}")
        else:
            lines.append(s)
    return "\n".join(lines)

def llm_structured_extract(raw_text: str, endpoint: str = DEFAULT_LLM_ENDPOINT, model: str = DEFAULT_MODEL_NAME, timeout: int = 60) -> Dict[str, List[Dict[str, Optional[str]]]]:
    cleaned = _preprocess_for_llm(raw_text)
    # Build chat-style payload
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": cleaned}
        ],
        "temperature": 0.0,
        "max_tokens": 1024
    }

    # Try chat completion
    try:
        resp = requests.post(endpoint, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content") or data.get("choices", [{}])[0].get("text", "")
        if not content:
            return {}
        # Parse JSON
        try:
            return json.loads(content)
        except Exception:
            # try to locate first JSON object in text
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(content[start:end+1])
                except Exception:
                    return {}
        return {}
    except Exception as e:
        print(f"[llm_extractor] LLM request failed: {e}")
        return {}
