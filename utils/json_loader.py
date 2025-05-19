# json_loader.py – rekursiver JSON-Scanner für alle AI-Zentrale-Verzeichnisse

import os
import json

ROOT_DIR = os.getenv("AI_ZENTRALE_ROOT") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

def load_config(filename: str) -> dict:
    """
    Sucht rekursiv nach einer Datei mit exakt diesem Namen und lädt sie als JSON.
    Gibt ein leeres Dict zurück, falls Datei nicht gefunden oder fehlerhaft ist.
    """
    for dirpath, _, filenames in os.walk(ROOT_DIR):
        if filename in filenames:
            try:
                path = os.path.join(dirpath, filename)
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"❌ Fehler beim Laden von {filename}: {e}")
                return {}
    print(f"⚠️ Datei {filename} nicht gefunden.")
    return {}

def list_all_jsons() -> list:
    """
    Gibt eine Liste aller .json-Dateien in AI-Zentrale zurück (rekursiv).
    """
    json_files = []
    for dirpath, _, filenames in os.walk(ROOT_DIR):
        for f in filenames:
            if f.endswith(".json"):
                json_files.append(os.path.join(dirpath, f))
    return json_files
