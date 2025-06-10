# main_controller.py – KI-Zentrale Modulstarter mit FastAPI Lifespan

import json
import importlib
import os
import subprocess
import sys
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

CONFIG_PATH = "config/system_modules.json"
processes = []

def load_json_file(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Datei {path}: {e}")
        return []

def load_active_modules():
    modules = load_json_file(CONFIG_PATH)
    print(f"📦 Lade {len(modules)} Modul(e) aus system_modules.json")
    return [
        m for m in modules
        if m.get("active") is True and m.get("type", "library") != "separator"
    ]

def run_module(module: dict):
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
            print(f"   → Server-Modul läuft auf Port {port} (PID: {proc.pid})")
        else:
            importlib.import_module(import_path)
            print(f"   → ✅ Library-Modul erfolgreich importiert.")
    except ModuleNotFoundError as e:
        print(f"❌ MODUL NICHT GEFUNDEN – {filename} | Pfad: {import_path}")
        print(f"   🔎 Mögliche Ursache: Falscher Pfad oder Datei nicht im Container")
        print(f"   💥 Exception: {e}")
    except Exception as e:
        print(f"❌ Fehler beim Starten von {filename} (Pfad: {import_path})")
        print(f"   💥 Exception: {e}")

# Lifespan-Handler für sauberen Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starte MAIN CONTROLLER (lifespan) ...")
    modules = load_active_modules()
    for module in modules:
        run_module(module)
    yield
    print("🛑 Lifespan beendet. Controller wird gestoppt.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def status():
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len(processes)
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
