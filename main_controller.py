# main_controller.py – Zentraler Einstiegspunkt für AI-ZENTRALE

import json
import os
from importlib import import_module
from chainlit.cli.main import run_chainlit  # Chainlit direkt ausführen

# Systemmodule laden
CONFIG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/system_modules.json"

def load_active_modules():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        modules = json.load(f)
    return [m for m in modules if m.get("active")]

def start_chainlit():
    print("🚀 Starte Chainlit Interface auf Port 8000...")
    run_chainlit(path="ai_zentrale/modules/input_interfaces/chainlit.py", port=8000)

def start_all_modules():
    active_modules = load_active_modules()
    for module in active_modules:
        if module["filename"] == "chainlit.py":
            # Chainlit wird separat als Server gestartet
            start_chainlit()
        else:
            try:
                import_path = module["import_path"]
                import_module(import_path)
                print(f"✅ Modul geladen: {import_path}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {module['filename']}: {str(e)}")

if __name__ == "__main__":
    print("📦 Starte AI-ZENTRALE über main_controller.py...")
    start_all_modules()
