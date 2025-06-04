# agents/Infrastructure_Agents/TriggerAgent/trigger_custom_action.py

from datetime import datetime
from utils.json_loader import load_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import (
    log_trigger_execution,
    log_trigger_error
)

# 🔐 Sichere Initialisierung
try:
    ACTION_MAP = load_json("trigger_action_map.json")
    if "error" in ACTION_MAP:
        ACTION_MAP = {}
except:
    ACTION_MAP = {}

# ▶ Führt eine definierte Aktion aus
def execute_trigger_action(trigger: dict) -> str:
    action_name = trigger.get("action", "undefined")
    trigger_name = trigger.get("name", "Unbenannt")

    if action_name == "undefined" or action_name not in ACTION_MAP:
        log_trigger_error(trigger_name, f"Aktionsname '{action_name}' unbekannt oder nicht definiert.")
        return f"❌ Unbekannte Aktion: '{action_name}'"

    try:
        module_path = ACTION_MAP[action_name]["module"]
        function_name = ACTION_MAP[action_name]["function"]
        module = __import__(module_path, fromlist=[function_name])
        function = getattr(module, function_name)
        result = function(trigger)
        log_trigger_execution(trigger_name, [action_name], datetime.now().isoformat())
        return f"{action_name} → {result}"

    except Exception as e:
        log_trigger_error(trigger_name, f"❌ Fehler bei Aktion '{action_name}': {e}")
        return f"{action_name} ❌ Fehler: {e}"

# ▶ Benutzerdefinierte Trigger aus Konfig
def check_custom_trigger(config: dict) -> list:
    results = []
    for trig in config.get("custom_triggers", []):
        if not trig.get("enabled", True):
            continue
        results.append({
            "type": "manual_trigger",
            "name": trig.get("name", "unnamed_custom_trigger"),
            "source": "custom_config",
            "timestamp": datetime.utcnow().isoformat()
        })
    return results
