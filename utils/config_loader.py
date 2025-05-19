# config_loader.py

import os
import json

CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Config"


def load_config(filename: str) -> dict:
    """
    Lädt eine JSON-Konfigurationsdatei aus dem zentralen Config-Verzeichnis.
    Gibt ein leeres Dict zurück, falls Datei fehlt oder ungültig ist.
    """
    try:
        path = os.path.join(CONFIG_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden von {filename}: {e}")
        return {}


def list_all_configs(extension: str = ".json") -> list:
    """
    Gibt eine Liste aller .json-Dateien im CONFIG_DIR zurück.
    """
    try:
        return [f for f in os.listdir(CONFIG_DIR) if f.endswith(extension)]
    except Exception as e:
        print(f"❌ Fehler beim Auflisten der Configs: {e}")
        return []
