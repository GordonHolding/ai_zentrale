# main_controller.py – mit Startup-Report, Fehlerprotokoll und erweitertem Healthcheck
# ✅ Unterstützt agent, utility, server, frontend
# ✅ Nutzt load_json_from_gdrive für Direktzugriff über Drive-ID
# ✅ Healthcheck prüft: App, Module, Prozesse, Credentials, Google Drive, Systemressourcen
# ✅ Bereit für sofortige Erweiterung (REST-Monitoring, Logging etc.)

import os
import sys
import subprocess
import importlib
from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils.json_loader import load_json_from_gdrive
from modules.authentication.google_utils import get_drive_service, get_service_account_credentials

try:
    import psutil  # Für Systemressourcen-Healthcheck
except ImportError:
    psutil = None  # Fallback, falls Paket nicht installiert ist

CONFIG_FILENAME = "system_modules.json"
processes = []
startup_errors = []
startup_success = []

def load_active_modules():
    """
    Lädt aktive Module aus system_modules.json, ignoriert fehlerhafte Inhalte.
    """
    modules = load_json_from_gdrive(CONFIG_FILENAME)
    if not isinstance(modules, list):
        print(f"⚠️  Fehlerhafte Konfiguration in {CONFIG_FILENAME}: {modules}")
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
    """
    Quick-Status: Zeigt Basisinfos zum Main Controller und Modulen.
    """
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len([p for p in processes if getattr(p, "poll", lambda: 0)() is None]),
        "module_erfolgreich": len(startup_success),
        "module_fehlerhaft": len(startup_errors)
    }

@app.get("/status/summary")
def status_summary():
    """
    Zeigt detailliert an, welche Module erfolgreich/fehlerhaft gestartet sind.
    """
    return {
        "erfolg": startup_success,
        "fehler": startup_errors
    }

@app.get("/health")
def healthcheck():
    """
    Erweiterter Healthcheck für System, Prozesse, Google Drive, Credentials, Module.
    """
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

    # 4. Systemressourcen (optional, falls psutil vorhanden)
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
        system_status = {"info": "psutil nicht installiert, keine Systemdaten verfügbar."}

    # 5. Letzte Fehler
    last_errors = startup_errors[-3:] if startup_errors else []

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
        "letzte_fehler": last_errors
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
