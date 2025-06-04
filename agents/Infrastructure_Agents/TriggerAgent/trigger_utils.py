# agents/Infrastructure_Agents/TriggerAgent/trigger_utils.py

from datetime import datetime
from utils.json_loader import load_json, write_json

# 🪵 Log für Erfolg
def log_trigger_execution(trigger_name: str, items: list, timestamp: str):
    log_entry = {
        "trigger": trigger_name,
        "items": items,
        "timestamp": timestamp
    }
    log_data = load_json("trigger_execution_log.json")
    if not isinstance(log_data, dict) or "error" in log_data:
        log_data = {}
    log_data["entries"] = log_data.get("entries", []) + [log_entry]
    write_json("trigger_execution_log.json", log_data)

# ❌ Fehlerlog (traceback optional!)
def log_trigger_error(trigger_name: str, error: str, traceback_str: str = ""):
    error_entry = {
        "trigger": trigger_name,
        "error": error,
        "traceback": traceback_str,
        "timestamp": datetime.utcnow().isoformat()
    }
    error_data = load_json("trigger_errors.json")
    if not isinstance(error_data, dict) or "error" in error_data:
        error_data = {}
    error_data["errors"] = error_data.get("errors", []) + [error_entry]
    write_json("trigger_errors.json", error_data)

# 🔁 Triggerstatus aktualisieren
def update_trigger_state(state_file: str, triggered_items: list, timestamp: str):
    state_data = load_json(state_file)
    if not isinstance(state_data, dict) or "error" in state_data:
        state_data = {}
    state_data["last_triggered"] = timestamp
    state_data["last_items"] = triggered_items
    write_json(state_file, state_data)

# ⚠️ Routingfehler
def log_routing_error(trigger: dict, error_msg: str):
    print(f"❌ Fehler beim Routing von Trigger {trigger.get('name')}: {error_msg}")
