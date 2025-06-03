# trigger_utils.py

from datetime import datetime
from utils.json_loader import load_json, write_json

# 🪵 Protokolliert erfolgreiche Triggerausführung
def log_trigger_execution(trigger_name: str, items: list, timestamp: str):
    log_entry = {
        "trigger": trigger_name,
        "items": items,
        "timestamp": timestamp
    }

    log_data = load_json("trigger_execution_log.json")
    if isinstance(log_data, dict) and "error" not in log_data:
        log_data.setdefault("entries", []).append(log_entry)
    else:
        log_data = {"entries": [log_entry]}

    write_json("trigger_execution_log.json", log_data)

# ❌ Protokolliert Trigger-Fehler (inkl. Traceback)
def log_trigger_error(trigger_name: str, error: str, traceback_str: str):
    error_entry = {
        "trigger": trigger_name,
        "error": error,
        "traceback": traceback_str,
        "timestamp": datetime.utcnow().isoformat()
    }

    error_data = load_json("trigger_errors.json")
    if isinstance(error_data, dict) and "error" not in error_data:
        error_data.setdefault("errors", []).append(error_entry)
    else:
        error_data = {"errors": [error_entry]}

    write_json("trigger_errors.json", error_data)

# 🔁 Speichert den letzten Triggerzustand für Statusüberwachung
def update_trigger_state(state_file: str, triggered_items: list, timestamp: str):
    state_data = load_json(state_file)
    if "error" in state_data or not isinstance(state_data, dict):
        state_data = {}

    state_data.update({
        "last_triggered": timestamp,
        "last_items": triggered_items
    })

    write_json(state_file, state_data)
