# main_controller.py – Smarter Startup-Controller mit klarer Fehlerausgabe & Reporting
# ✅ Unterstützt agent, utility, server, frontend (beliebig erweiterbar)
# ✅ Lädt Konfiguration direkt aus Google Drive (per Drive-ID via load_json_from_gdrive)
# ✅ Protokolliert erfolgreiche und fehlgeschlagene Modulstarts mit Fehlerdetails
# ✅ Zeigt Fehlerursachen und Stacktrace im Render-Log (perfekt für Remote-Debugging)
# ✅ Status- und Summary-Endpoints für Monitoring

import os
import sys
import subprocess
import importlib
import traceback
from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils.json_loader import load_json_from_gdrive  # Direkt aus Drive laden

CONFIG_FILENAME = "system_modules.json"
processes = []         # Gestartete Server-Prozesse (z.B. Subprozesse)
startup_errors = []    # Fehlerprotokoll (dicts mit Details)
startup_success = []   # Erfolgreiche Modulstarts (dicts mit Details)

def load_active_modules():
    """
    Lädt aktive Module aus der system_modules.json (Google Drive).
    Nur Module mit 'active': True und erlaubtem Typ werden berücksichtigt.
    """
    modules = load_json_from_gdrive(CONFIG_FILENAME)
    if not isinstance(modules, list):
        print(f"⚠️  Fehlerhafte Konfiguration in {CONFIG_FILENAME}: {modules}")
        return []
    print(f"📦 Lade {len(modules)} Modul(e) aus {CONFIG_FILENAME}")
    # Nur gewünschte Typen und aktive Module zulassen
    return [
        m for m in modules
        if m.get("active") is True and m.get("type") in {"agent", "utility", "server", "frontend"}
    ]

def run_module(module: dict):
    """
    Startet ein Modul je nach Typ:
      - 'server' wird als Subprozess mit eigenem Port gestartet
      - 'agent', 'utility', 'frontend' werden per importlib importiert
    Fehler werden umfassend geloggt (inkl. Stacktrace für Remote-Debugging).
    """
    import_path = module.get("import_path", "")
    filename = module.get("filename", "Unbekannt")
    mod_type = module.get("type", "agent")
    try:
        print(f"🟢 Starte Modul: {import_path} ({mod_type})")
        if mod_type == "server":
            # Pfad in Dateisystemform bringen (z.B. "my.module" -> "my/module.py")
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
        # Spezielles Logging für fehlende Module
        msg = f"❌ MODUL NICHT GEFUNDEN – {filename} | Pfad: {import_path}\n↪️ Grund: {e}"
        print(msg)
        traceback.print_exc()
        startup_errors.append({
            "module": filename,
            "reason": repr(e),
            "type": mod_type
        })
    except Exception as e:
        # Alle anderen Fehler (inkl. Stacktrace für präzises Debugging)
        msg = f"❌ Fehler beim Starten von {filename} (Pfad: {import_path})\n↪️ Grund: {e}"
        print(msg)
        traceback.print_exc()
        startup_errors.append({
            "module": filename,
            "reason": repr(e),
            "type": mod_type
        })

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI-Lebenszyklus: Lädt und startet alle aktiven Module beim Serverstart.
    Loggt Zusammenfassung der Ergebnisse.
    """
    print("🚀 Starte MAIN CONTROLLER (lifespan) ...")
    modules = load_active_modules()
    for module in modules:
        run_module(module)
    print("🔍 Startup abgeschlossen.")
    print(f"✅ Erfolgreich gestartet: {len(startup_success)}")
    print(f"❌ Fehlgeschlagen: {len(startup_errors)}")
    yield
    print("🛑 Lifespan beendet. Controller wird gestoppt.")

# FastAPI App mit Lebenszyklus
app = FastAPI(lifespan=lifespan)

@app.get("/")
def status():
    """
    Kurzer Status-Check:
      - Anzahl laufender Prozesse
      - Anzahl erfolgreicher & fehlgeschlagener Modulstarts
    """
    return {
        "status": "Main Controller läuft",
        "aktive_prozesse": len(processes),
        "module_erfolgreich": len(startup_success),
        "module_fehlerhaft": len(startup_errors)
    }

@app.get("/status/summary")
def status_summary():
    """
    Detailübersicht:
      - Liste der erfolgreichen und fehlgeschlagenen Module (inkl. Fehlerursache)
    """
    return {
        "erfolg": startup_success,
        "fehler": startup_errors
    }

if __name__ == "__main__":
    # Lokaler Start für Entwicklung – auf Render wird meist über Uvicorn-Entrypoint gebootet!
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
