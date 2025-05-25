# main_controller.py – Zentrale Steuerinstanz der AI-ZENTRALE

import json
import importlib
import os
import time

from utils.json_loader import load_config

# 🔄 Lade aktivierte Module direkt aus GitHub-Pfad
def load_active_modules():
    modules = load_config("config/system_modules.json")
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
