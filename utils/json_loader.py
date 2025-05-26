# json_loader.py – JSON-Verwaltung für AI-ZENTRALE (rekursiv, GPT-kompatibel)

import os
import json

CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

# 🔍 JSON-Datei anhand ihres Namens laden (außer system_modules.json)
def load_json(filename: str) -> dict:
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

# 📝 JSON-Datei schreiben (vollständig überschreiben)
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
        print(f"❌ Fehler beim Schreiben von {filename}: {e}")
        return False
