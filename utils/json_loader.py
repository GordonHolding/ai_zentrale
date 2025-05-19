# json_loader.py – Zentrale Verwaltung aller JSON-Dateien im System (rekursiv, GPT-kompatibel)

import os
import json

# Basisverzeichnis, in dem alle .json-Dateien liegen können (rekursiv durchsucht)
CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

def load_config(filename: str) -> dict:
    """
    Lädt eine JSON-Konfigurationsdatei aus dem zentralen Verzeichnis (CONFIG_DIR).
    Gibt ein leeres Dict zurück, falls Datei fehlt oder ungültig ist.
    """
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                full_path = os.path.join(root, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        return {"error": f"{filename} nicht gefunden in {CONFIG_DIR}"}
    except Exception as e:
        return {"error": f"Fehler beim Laden von {filename}: {e}"}

def list_all_configs(extension: str = ".json") -> list:
    """
    Gibt eine Liste aller .json-Dateien im gesamten CONFIG_DIR zurück.
    """
    result = []
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(extension):
                    result.append(os.path.join(root, file))
        return result
    except Exception as e:
        print(f"❌ Fehler beim Auflisten der Configs: {e}")
        return []

def get_json_by_keyword(keyword: str) -> dict:
    """
    Findet eine JSON-Datei im CONFIG_DIR, deren Dateiname das Keyword enthält.
    Gibt das geladene Dict zurück oder eine Fehlermeldung.
    """
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(".json") and keyword.lower() in file.lower():
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
        return {"error": f"Keine passende JSON-Datei mit Keyword '{keyword}' gefunden."}
    except Exception as e:
        return {"error": f"Fehler beim Suchen nach JSON: {e}"}
