# text_templates.py – lädt Textvorlagen aus output_map.json

import json

OUTPUT_MAP_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/output_map.json"

def load_text_template(template_key):
    try:
        with open(OUTPUT_MAP_PATH, "r", encoding="utf-8") as f:
            templates = json.load(f)
        return templates.get(template_key)
    except Exception:
        return None
