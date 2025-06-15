# main_controller.py – Startup-Manager & System-Monitor mit Healthcheck und RAM-Überwachung

import os
import sys
import subprocess
import importlib
from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils.json_loader import load_json_from_gdrive
from modules.authentication.google_utils import get_drive_service, get_service_account_credentials
from agents.GPTAgent.context_memory import get_all_context
from utils.json_index_status import get_json_index_status  # ✅ NEU

# Optional: Systemressourcen
try:
    import psutil
except ImportError:
    psutil = None

# Optional: Cleanup-Report
try:
    from utils.render_disk_cleaner import get_last_cleanup_report
except ImportError:
    def get_last_cleanup_report():
        return {"status": "not available"}

CONFIG_FILENAME = "system_modules.json"
processes = []
startup_errors = []
startup_success = []

# 🔄 Aktive Module laden
def load_active_modules():
    modules = load_json_from_gdrive(CONFIG_FILENAME)
    if not isinstance(modules, list):
        print(f"⚠️ Fehlerhafte Konfiguration in {CONFIG_FILENAME}: {modules}")
        return []
    print(f"📦 Lade {len(modules)} Modul(e) aus {CONFIG_FILENAME}")
    return [
        m for m in modules
        if m.get("active") is True and m.get("type") in {"agent", "utility", "server", "frontend"}
    ]

# ▶️ Module starten oder importieren
def run_module(module: dict):
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

# 🔁 Lebenszyklus FastAPI
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

# ▶️ Basisstatus
@app.get("/")
def status():
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len([p for p in processes if getattr(p, "poll", lambda: 0)() is None]),
        "module_erfolgreich": len(startup_success),
        "module_fehlerhaft": len(startup_errors)
    }

# ▶️ Zusammenfassung
@app.get("/status/summary")
def status_summary():
    return {
        "erfolg": startup_success,
        "fehler": startup_errors
    }

# ✅ Healthcheck
@app.get("/health")
def healthcheck():
    # 1. Service-Account-Credentials
    try:
        creds = get_service_account_credentials()
        credentials_status = "ok"
    except Exception as e:
        credentials_status = f"Fehler: {e}"

    # 2. Google Drive erreichbar?
    try:
        service = get_drive_service()
        service.files().list(pageSize=1).execute()
        drive_status = "ok"
    except Exception as e:
        drive_status = f"Fehler: {e}"

    # 3. Subprozess-Status
    proc_status = []
    for proc in processes:
        try:
            status = "running" if proc.poll() is None else f"exited ({proc.returncode})"
        except Exception:
            status = "unknown"
        proc_status.append({"pid": getattr(proc, "pid", None), "status": status})

    # 4. Systemressourcen
    if psutil:
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            system_status = {
                "cpu_percent": cpu,
                "mem_percent": mem.percent,
                "disk_percent": disk.percent,
            }
        except Exception as e:
            system_status = {"error": str(e)}
    else:
        system_status = {"info": "psutil nicht installiert"}

    # 5. Letzte Fehler
    last_errors = startup_errors[-3:] if startup_errors else []

    # 6. Cleanup-Report
    cleanup_report = get_last_cleanup_report()

    # 7. RAM-Kontextstatus
    try:
        context_data = get_all_context()
        ram_context = {
            "total_keys": len(context_data),
            "keys": list(context_data.keys()),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        ram_context = {"error": str(e)}

    # 8. JSON-Index-Status
    try:
        json_index_status = get_json_index_status()
    except Exception as e:
        json_index_status = {"error": str(e)}

    # 🔎 Kompletter Health-Bericht
    return {
        "app": "ok",
        "credentials": credentials_status,
        "google_drive": drive_status,
        "prozesse": proc_status,
        "system": system_status,
        "module": {
            "erfolgreich": len(startup_success),
            "fehlerhaft": len(startup_errors)
        },
        "letzte_fehler": last_errors,
        "cleanup_report": cleanup_report,
        "ram_context": ram_context,
        "json_index_status": json_index_status  # ✅ Eingebaut!
    }

# ▶️ Lokaler Start (Render-ready)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
