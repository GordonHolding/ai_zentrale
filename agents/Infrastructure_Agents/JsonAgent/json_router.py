# json_router.py – GPT-Befehle analysieren und systemisch weiterreichen

from agents.Infrastructure_Agents.JsonAgent.json_agent import update_json_entry
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_index
from agents.Infrastructure_Agents.JsonAgent.json_validator import validate_entry

# 🔍 Analyse & Routing eingehender GPT-Anweisungen zu JSON-Dateien
def handle_json_instruction(instruction: str) -> str:
    try:
        instruction_lower = instruction.lower()
        index = get_json_index()

        # Beispiel: TriggerConfig aktualisieren
        if "trigger_config" in instruction_lower and "füge" in instruction_lower:
            key = "scan_drive"
            value = {
                "active": True,
                "interval_hours": 72,
                "target_module": "agents.Infrastructure_Agents.TriggerAgent.trigger_triggers",
                "target_function": "trigger_scan_drive"
            }
            return update_json_entry("trigger_config", key, value, overwrite=False)

        # 🔄 Dynamischer JSON-Index-Zugriff
        for file_key in index.keys():
            if file_key in instruction_lower:
                return f"🧭 JSON-Datei erkannt: '{file_key}' – was genau soll geändert werden?"

        return "⚠️ Anweisung unklar oder kein gültiger JSON-Kontext erkannt."

    except Exception as e:
        return f"❌ Fehler beim Verarbeiten der JSON-Anweisung: {e}"
