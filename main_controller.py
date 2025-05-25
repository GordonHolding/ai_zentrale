# main_controller.py – Zentrale Steuerinstanz der AI-ZENTRALE

import json
import importlib
import os
import time

from modules.utils.json_loader import load_json_file

# 🔄 Lade aktivierte Module
def load_active_modules():
    config_path = "0.3 AI-Regelwerk & Historie/Systemregeln/system_modules.json"
    modules = load_json_file(config_path)
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
