# main_controller.py – KI-Zentrale Modulstarter (FastAPI + Lifespan) – final & optimiert

import os
import sys
import json
import threading
import subprocess
import importlib
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

CONFIG_PATH = "config/system_modules.json"
processes = []

# 📥 JSON-Datei laden
def load_json_file(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden der Datei {path}: {e}")
        return []

# 🔍 Alle aktiven Module aus der Konfig laden
def load_active_modules() -> list:
    modules = load_json_file(CONFIG_PATH)
    return [
        m for m in modules
        if m.get("active") is True and m.get("type", "library") != "separator"
    ]

# 🚀 Module starten (Library & Server)
def run_modules():
    modules = load_active_modules()
    print(f"📦 Lade {len(modules)} aktive Modul(e) ...")
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

# 🔄 Startup/Shutdown mit lifespan (zukunftssicher)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starte MAIN CONTROLLER (manuell) ...")
    thread = threading.Thread(target=run_modules)
    thread.daemon = True
    thread.start()
    yield
    print("🛑 MAIN CONTROLLER Shutdown eingeleitet ...")
    for proc in processes:
        proc.terminate()
        print(f"   → Prozess {proc.pid} beendet.")

# 🌐 Webservice + Status-Check
app = FastAPI(lifespan=lifespan)

@app.get("/")
def status():
    return {"status": "Main Controller läuft", "prozesse": len(processes)}

# 🖥️ Lokaler Start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main_controller:app", host="0.0.0.0", port=port, reload=False)
