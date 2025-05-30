# json_loader.py – Zentrale JSON-Verwaltung für AI-ZENTRALE (GPT-kompatibel, rekursiv, fehlertolerant)

import os
import json

# 🗂️ Zentrales Root-Verzeichnis aller JSON-Dateien
CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

# 🔄 JSON-Datei laden (GPT-sicher, systemtolerant)
def load_json(filename: str) -> dict:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                path = os.path.join(root, filename)
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        return {"error": f"📂 Datei '{filename}' nicht gefunden in {CONFIG_DIR}"}
    except Exception as e:
        return {"error": f"❌ Fehler beim Laden von '{filename}': {e}"}

# 💾 JSON-Datei schreiben (komplett überschreiben, mit Formatierung)
def write_json(filename: str, data: dict) -> dict:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                path = os.path.join(root, filename)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return {"success": f"✅ Datei '{filename}' erfolgreich aktualisiert."}
        return {"error": f"📂 Datei '{filename}' nicht gefunden zum Schreiben."}
    except Exception as e:
        return {"error": f"❌ Fehler beim Schreiben von '{filename}': {e}"}

# 📁 Liste alle JSON-Dateien im gesamten AI-ZENTRALE-Verzeichnis
def list_all_configs(extension: str = ".json") -> list:
    result = []
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(extension):
                    result.append(os.path.join(root, file))
        return result
    except Exception as e:
        return [f"❌ Fehler beim Auflisten der JSON-Dateien: {e}"]

# 🔎 Finde erste passende Datei mit Keyword im Namen
def get_json_by_keyword(keyword: str) -> dict:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(".json") and keyword.lower() in file.lower():
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
        return {"error": f"🔍 Keine passende Datei mit Keyword '{keyword}' gefunden."}
    except Exception as e:
        return {"error": f"❌ Fehler beim JSON-Zugriff mit Keyword: {e}"}
