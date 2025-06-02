# trigger_custom_action.py

from utils.json_loader import load_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_execution, log_error

# Lade Trigger-Aktionen aus zentraler Konfiguration
ACTION_MAP = load_json("trigger_action_map.json")

def execute_trigger_action(trigger):
    """
    Führt eine Aktion aus, die im Trigger-Objekt spezifiziert ist.
    Der konkrete Aktionsname muss in trigger["action"] stehen.
    """
    action_name = trigger.get("action", "undefined")
    trigger_name = trigger.get("name", "Unbenannt")

    if action_name == "undefined" or action_name not in ACTION_MAP:
        log_error(trigger_name, f"Aktionsname '{action_name}' unbekannt oder nicht definiert.")
        return f"❌ Unbekannte Aktion: '{action_name}'"

    try:
        module_path = ACTION_MAP[action_name]["module"]
        function_name = ACTION_MAP[action_name]["function"]

        # Dynamisches Importieren der Funktion
        module = __import__(module_path, fromlist=[function_name])
        function = getattr(module, function_name)

        # Optional: Übergabe des gesamten Trigger-Objekts
        result = function(trigger)

        log_execution(trigger_name, f"✅ Aktion '{action_name}' erfolgreich ausgeführt.")
        return f"{action_name} → {result}"

    except Exception as e:
        log_error(trigger_name, f"❌ Fehler bei Aktion '{action_name}': {e}")
        return f"{action_name} ❌ Fehler: {e}"
