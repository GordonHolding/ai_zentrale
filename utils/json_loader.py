# json_loader.py

import os
import json

# Standardverzeichnis für alle systemweiten JSON-Dateien
JSON_DIR = os.getenv("JSON_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Config"

def load_json(filename: str) -> dict:
    """
    Lädt eine JSON-Datei aus dem zentralen JSON-Verzeichnis.
    Gibt ein leeres Dict zurück, falls Datei fehlt oder ungültig ist.
    """
    try:
        path = os.path.join(JSON_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden von {filename}: {e}")
        return {}

def list_json_files(extension: str = ".json") -> list:
    """
    Gibt eine Liste aller .json-Dateien im JSON_DIR zurück.
    """
    try:
        return [f for f in os.listdir(JSON_DIR) if f.endswith(extension)]
    except Exception as e:
        print(f"❌ Fehler beim Auflisten der JSON-Dateien: {e}")
        return []
