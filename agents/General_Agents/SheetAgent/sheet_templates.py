# sheet_templates.py – lädt Templates aus sheet_template_map.json

import json

TEMPLATE_MAP_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/sheet_template_map.json"

def load_sheet_template(template_key):
    try:
        with open(TEMPLATE_MAP_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(template_key)
    except Exception:
        return None
