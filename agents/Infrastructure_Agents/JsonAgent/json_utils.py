# json_utils.py – Hilfsmethoden für Lesen, Schreiben, Validieren von JSON-Dateien

import os
import json

from modules.utils.json_loader import JSON_DIR

def load_json(filename):
    try:
        path = os.path.join(JSON_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden von {filename}: {e}")
        return {}

def write_json(filename, data):
    path = os.path.join(JSON_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
