# main_controller.py – mit Startup-Report & Fehlerprotokoll
# ✅ Unterstützt agent, utility, server, frontend
# ✅ Nutzt safe_load_json für robustes Startup
# ✅ Bereit für sofortige Erweiterung (REST-Monitoring, Logging etc.)

import os
import sys
import subprocess
import importlib
from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils.json_loader import safe_load_json

CONFIG_FILENAME = "system_modules.json"
processes = []
startup_errors = []
startup_success = []

def load_active_modules():
    """
    Lädt aktive Module aus system_modules.json, ignoriert fehlerhafte Inhalte.
    """
    modules = safe_load_json(CONFIG_FILENAME)
    if not isinstance(modules, list):
        print(f"⚠️  Fehlerhafte Konfiguration in {CONFIG_FILENAME}: {modules.get('error', 'Unbekannter Fehler')}")
        return []
    print(f"📦 Lade {len(modules)} Modul(e) aus {CONFIG_FILENAME}")
    return [
        m for m in modules
        if m.get("active") is True and m.get("type") in {"agent", "utility", "server", "frontend"}
    ]

def run_module(module: dict):
    """
    Startet das angegebene Modul je nach Typ (import oder subprocess).
    """
    import_path = module.get("import_path", "")
    filename = module.get("filename", "Unbekannt")
    mod_type = module.get("type", "agent")

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
            startup_success.append({
                "module": filename,
                "status": "running",
                "port": port,
                "type": "server"
            })

        elif mod_type in {"agent", "utility", "frontend"}:
            importlib.import_module(import_path)
            print(f"   → ✅ Modul erfolgreich importiert.")
            startup_success.append({
                "module": filename,
                "status": "imported",
                "type": mod_type
            })

        else:
            raise ValueError(f"Unbekannter Modultyp: {mod_type}")

    except ModuleNotFoundError as e:
        msg = f"❌ MODUL NICHT GEFUNDEN – {filename} | Pfad: {import_path}"
        print(msg)
        startup_errors.append({
            "module": filename,
            "reason": str(e),
            "type": mod_type
        })

    except Exception as e:
        msg = f"❌ Fehler beim Starten von {filename} (Pfad: {import_path})"
        print(msg)
        startup_errors.append({
            "module": filename,
            "reason": str(e),
            "type": mod_type
        })

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starte MAIN CONTROLLER (lifespan) ...")
    modules = load_active_modules()
    for module in modules:
        run_module(module)
    print("🔍 Startup abgeschlossen.")
    print(f"✅ Erfolgreich gestartet: {len(startup_success)}")
    print(f"❌ Fehlgeschlagen: {len(startup_errors)}")
    yield
    print("🛑 Lifespan beendet. Controller wird gestoppt.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def status():
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len(processes),
        "module_erfolgreich": len(startup_success),
        "module_fehlerhaft": len(startup_errors)
    }

@app.get("/status/summary")
def status_summary():
    return {
        "erfolg": startup_success,
        "fehler": startup_errors
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
