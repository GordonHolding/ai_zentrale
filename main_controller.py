# main_controller.py – Optimierte zentrale Steuerinstanz der AI-ZENTRALE

import json
import importlib
import os
import subprocess
import sys
import time

CONFIG_PATH = "config/system_modules.json"

def load_json_file(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Datei {path}: {e}")
        return []

def load_active_modules():
    modules = load_json_file(CONFIG_PATH)
    return [
        m for m in modules
        if m.get("active") is True and m.get("type", "library") != "separator"
    ]

def run_modules():
    modules = load_active_modules()
    processes = []
    for module in modules:
        try:
            import_path = module["import_path"]
            mod_type = module.get("type", "library")
            print(f"🟢 Starte Modul: {import_path} ({mod_type})")

            if mod_type == "server":
                # Pfad zur .py-Datei aus Importpfad berechnen
                script_path = import_path.replace('.', os.sep) + ".py"
                port = str(module.get("port", 8000))

                proc = subprocess.Popen(
                    [sys.executable, script_path, "--port", port],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=os.environ.copy()
                )
                processes.append(proc)
                print(f"   → Server-Modul läuft als Subprozess auf Port {port} (PID: {proc.pid})")
            else:
                importlib.import_module(import_path)
                print(f"   → Library-Modul importiert.")
        except Exception as e:
            print(f"❌ Fehler beim Starten von {module.get('filename', 'Unbekannt')}: {e}")

    try:
        print("🛑 Zum Beenden: [STRG+C]")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stoppe alle Subprozesse ...")
        for proc in processes:
            proc.terminate()
        print("✅ Alle Module gestoppt.")

if __name__ == "__main__":
    print("🚀 Starte MAIN CONTROLLER ...")
    time.sleep(1)
    run_modules()
