# main_controller.py – Zentrale Steuerinstanz der AI-ZENTRALE

import json
import importlib
import os
import time

# 🔁 Direkter Loader für GitHub-Dateien
def load_json_file(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Datei {path}: {e}")
        return []

# 🔄 Lade aktivierte Module direkt aus GitHub (config/system_modules.json)
def load_active_modules():
    modules = load_json_file("config/system_modules.json")
    return [m for m in modules if m.get("active") is True]

# ▶ Starte Module nacheinander
def run_modules():
    modules = load_active_modules()
    for module in modules:
        try:
            import_path = module["import_path"]
            print(f"🟢 Lade Modul: {import_path}")
            importlib.import_module(import_path)
        except Exception as e:
            print(f"❌ Fehler beim Laden von {import_path}: {e}")

if __name__ == "__main__":
    print("🚀 Starte MAIN CONTROLLER ...")
    time.sleep(1)
    run_modules()
