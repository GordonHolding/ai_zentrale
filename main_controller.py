import json
import importlib
import os
import subprocess
import sys
import time
from fastapi import FastAPI
import threading
import uvicorn

CONFIG_PATH = "system_modules.json"
app = FastAPI()
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
    return [
        m for m in modules
        if m.get("active") is True and m.get("type", "library") != "separator"
    ]

def run_modules():
    modules = load_active_modules()
    for module in modules:
        try:
            import_path = module["import_path"]
            mod_type = module.get("type", "library")
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
                print(f"   → Library-Modul importiert.")
        except Exception as e:
            print(f"❌ Fehler beim Starten von {module.get('filename', 'Unbekannt')}: {e}")

# Dummy API-Endpunkt für Render
@app.get("/")
def status():
    return {"status": "Main Controller läuft", "prozesse": len(processes)}

# Modulstart als Hintergrundthread
def start_modules_async():
    thread = threading.Thread(target=run_modules)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    print("🚀 Starte MAIN CONTROLLER als Webservice (FastAPI + Agenten) ...")
    start_modules_async()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
