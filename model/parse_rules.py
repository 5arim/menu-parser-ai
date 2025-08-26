# parse_rules.py
from __future__ import annotations
import re
from typing import Dict, List, Optional

PAIR_RE = re.compile(r"(?P<item>.+?)\s+[•\.\-]*\s*(?P<price>(?:Rs\.?|₹|\$|€|£)?\s*\d{1,4}(?:[.,]\d{2})?(?:/\d{1,4})?)\s*$", re.IGNORECASE)

def rule_based_parse(text: str) -> Dict[str, List[dict]]:
    sections: dict = {"Uncategorized": []}
    current = "Uncategorized"
    for raw in (ln for ln in text.splitlines() if ln.strip()):
        line = raw.strip()
        if len(line) <= 30 and line.upper() == line and not any(ch.isdigit() for ch in line):
            current = line.title()
            sections.setdefault(current, [])
            continue
        m = PAIR_RE.match(line)
        if m:
            item = m.group("item").strip(" .-–—")
            price = m.group("price").strip()
            sections.setdefault(current, []).append({"item": item, "price": price, "notes": ""})
        else:
            if sum(ch.isalpha() for ch in line) / max(1, len(line)) > 0.5:
                sections.setdefault(current, []).append({"item": line, "price": "", "notes": ""})
            else:
                if sections.get(current):
                    sections[current][-1]["notes"] = (sections[current][-1].get("notes", "") + " " + line).strip()
                else:
                    sections.setdefault(current, []).append({"item": line, "price": "", "notes": ""})
    return {k: v for k, v in sections.items() if v}
