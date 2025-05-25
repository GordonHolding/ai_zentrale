# ===============================================
# 🧠 main_controller.py – Steuerzentrale der AI-Zentrale
# Enthält: Modulsteuerung, Logging, Dev-Modus, Healthcheck
# ===============================================

# 🔁 system_modules.json Loader
import importlib
import json
import os
import sys
import traceback
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config/system_modules.json')
LOG_PATH = os.path.join(BASE_DIR, 'controller_log.json')
HEALTH_PATH = os.path.join(BASE_DIR, 'health_status.json')

# 📅 Timestamp-Funktion
def timestamp():
    return datetime.utcnow().isoformat()

# 📜 Logging: controller_log.json
def log_entry(entries):
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.extend(entries)
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ❤️‍🩹 HealthCheck: health_status.json
def write_health_status(success, error_count):
    status = {
        "status": "ok" if error_count == 0 else "degraded",
        "active_modules": success,
        "errors": error_count,
        "timestamp": timestamp()
    }
    with open(HEALTH_PATH, "w") as f:
        json.dump(status, f, indent=4)

# 🔁 Module laden
def load_modules(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

# ▶ Modul starten (sofern main() vorhanden)
def run_module(import_path):
    try:
        mod = importlib.import_module(import_path)
        if hasattr(mod, "main"):
            mod.main()
            return "started", None
        else:
            return "skipped", "No main() found"
    except Exception as e:
        return "error", str(e)

# ✅ Dev-/Prod-Modus + Ausführung
def main():
    print("🚀 Initialisiere AI-ZENTRALE...")
    modules = load_modules(CONFIG_PATH)
    mode = "prod"
    selected_module = None

    if len(sys.argv) >= 3 and sys.argv[1] == "--dev":
        mode = "dev"
        selected_module = sys.argv[2]
        print(f"🧪 Dev-Modus aktiv: Starte nur {selected_module}")

    log = []
    success = 0
    errors = 0

    for module in modules:
        filename = module.get("filename")
        import_path = module.get("import_path")
        active = module.get("active", False)
        approval = module.get("approval_required", False)

        if mode == "dev" and filename != selected_module:
            continue

        if active:
            if approval:
                status = "waiting_for_approval"
                error_msg = "Approval required"
                print(f"🔒 {import_path} wartet auf Freigabe.")
            else:
                status, error_msg = run_module(import_path)
                if status == "started":
                    success += 1
                    print(f"✅ Gestartet: {import_path}")
                elif status == "error":
                    errors += 1
                    print(f"❌ Fehler in {import_path}: {error_msg}")
                else:
                    print(f"⚠ {import_path} übersprungen ({error_msg})")

            log.append({
                "module": import_path,
                "status": status,
                "error": error_msg,
                "timestamp": timestamp()
            })

    log_entry(log)
    write_health_status(success, errors)
    print(f"🏁 Fertig: {success} Module aktiv, {errors} Fehler.")

# ▶ Entry Point
if __name__ == "__main__":
    main()
