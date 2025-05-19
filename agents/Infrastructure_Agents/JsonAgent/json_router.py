# json_router.py – GPT-Befehle analysieren und weiterreichen

from agents.Infrastructure_Agents.JsonAgent.json_agent import update_json_entry

def handle_json_instruction(instruction: str) -> str:
    # einfache textbasierte Analyse – z. B. für: "Füge zu trigger_config X hinzu"
    try:
        if "trigger_config" in instruction and "füge" in instruction.lower():
            key = "scan_drive"
            value = {
                "active": True,
                "interval_hours": 72,
                "target_module": "agents.Infrastructure_Agents.TriggerAgent.trigger_triggers",
                "target_function": "trigger_scan_drive"
            }
            return update_json_entry("trigger_config", key, value, overwrite=False)
        return "❌ Anweisung nicht erkannt oder zu ungenau."
    except Exception as e:
        return f"❌ Fehler: {e}"
