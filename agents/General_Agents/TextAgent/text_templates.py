# text_templates.py – lädt Textvorlagen aus output_map.json

import json
import os

TEMPLATE_PATH = os.getenv("OUTPUT_MAP_PATH") or "0.3 AI-Regelwerk & Historie/Systemregeln/Config/output_map.json"

def load_text_template(template_key):
    """
    Lädt eine spezifische Textvorlage anhand des Keys.
    Gibt None zurück, wenn nicht gefunden oder bei Fehlern.
    """
    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            templates = json.load(f)
            return templates.get(template_key)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Textvorlage '{template_key}': {e}")
        return None
