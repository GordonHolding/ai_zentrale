# main_controller.py – KI-Zentrale Modulstarter (stabil, logging-optimiert)

import os
import sys
import json
import time
import threading
import importlib
import subprocess
from fastapi import FastAPI
import uvicorn

CONFIG_PATH = "config/system_modules.json"
app = FastAPI()
processes = []

# 📥 JSON laden mit Fehlerabfang
def load_json_file(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden von {path}: {e}")
        return []

# 📌 Aktive Module auslesen (ohne Trenner)
def load_active_modules() -> list:
    modules = load_json_file(CONFIG_PATH)
    return [
        m for m in modules
        if m.get("active") is True and m.get("type", "library") != "separator"
    ]

# 🚀 Module starten (Library & Server)
def run_modules():
    modules = load_active_modules()
    if not modules:
        print("⚠️  Keine aktiven Module gefunden in system_modules.json")
        return

    print(f"🔄 Lade {len(modules)} aktive Modul(e) ...")

    for module in modules:
        import_path = module.get("import_path", "")
        filename = module.get("filename", "Unbekannt")
        mod_type = module.get("type", "library")

        try:
            print(f"🟢 Starte Modul: {import_path} ({mod_type})")

            if mod_type == "server":
                script_path = import_path.replace('.', os.sep) + ".py"
                port = str(module.get("port", 8000))
                proc = subprocess.Popen(
                    [sys.executable, script_path, "--port", port],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=os.environ.copy()
                )
                processes.append(proc)
                print(f"   → 🌐 Server-Modul läuft auf Port {port} (PID: {proc.pid})")

            else:
                importlib.import_module(import_path)
                print(f"   → ✅ Library-Modul erfolgreich importiert.")

        except ModuleNotFoundError as e:
            print(f"❌ MODUL NICHT GEFUNDEN – {filename}")
            print(f"   🔎 Pfad: {import_path}")
            print(f"   💥 Exception: {e}")

        except Exception as e:
            print(f"❌ Fehler beim Laden von {filename} ({import_path})")
            print(f"   💥 Exception: {e}")

# 🔄 Hintergrundthread für Modulstart
def start_modules_async():
    thread = threading.Thread(target=run_modules)
    thread.daemon = True
    thread.start()

# 🔁 Wichtig für Render: FastAPI Startup-Trigger
@app.on_event("startup")
def startup_event():
    print("⚙️ FastAPI Startup → Module werden geladen ...")
    start_modules_async()

# 🩺 Status-Endpunkt für Render
@app.get("/")
def status():
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len(processes),
        "module": [p.pid for p in processes if p.poll() is None]
    }

# 🧪 Manuelles Starten lokal
if __name__ == "__main__":
    print("🚀 Starte MAIN CONTROLLER (manuell) ...")
    start_modules_async()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
