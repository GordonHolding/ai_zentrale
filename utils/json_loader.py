# json_loader.py – JSON-Verwaltung für AI-ZENTRALE (rekursiv, GPT-kompatibel)

import os
import json

# 🗂️ Root-Verzeichnis aller JSON-Dateien (rekursiv durchsucht)
CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

# 🔍 JSON-Datei anhand ihres Namens laden (außer system_modules.json)
def load_config(filename: str) -> dict:
    if filename == "system_modules.json":
        return {"error": "Zugriff auf system_modules.json ist nur über GitHub erlaubt."}
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                full_path = os.path.join(root, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        return {"error": f"{filename} nicht gefunden in {CONFIG_DIR}"}
    except Exception as e:
        return {"error": f"Fehler beim Laden von {filename}: {e}"}

# 📥 GPT-kompatibel: JSON-Datei laden (einfacher Shortcut für Agenten)
def load_json(filename: str) -> dict:
    return load_config(filename)

# 💾 GPT-kompatibel: JSON-Datei speichern
def write_json(filename: str, data: dict) -> bool:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                full_path = os.path.join(root, filename)
                with open(full_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
        return False
    except Exception as e:
        print(f"❌ Fehler beim Speichern von {filename}: {e}")
        return False

# 📁 Gibt alle .json-Dateien im gesamten AI-ZENTRALE-Verzeichnis zurück
def list_all_configs(extension: str = ".json") -> list:
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

# 🔎 Findet und lädt erste .json-Datei, deren Name ein Keyword enthält
def get_json_by_keyword(keyword: str) -> dict:
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
