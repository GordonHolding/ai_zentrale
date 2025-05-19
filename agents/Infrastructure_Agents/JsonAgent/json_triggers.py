# json_triggers.py – Beispiel für systemische Routine-Trigger

from agents.General_Agents.JsonAgent.json_utils import load_json
from agents.General_Agents.JsonAgent.json_config import JSON_CONFIG_LIST

def check_empty_keys():
    result = []
    for key, meta in JSON_CONFIG_LIST.items():
        data = load_json(meta["filename"])
        if not data:
            result.append(f"⚠️ {key} ist leer oder konnte nicht geladen werden.")
    return "\n".join(result) if result else "✅ Alle JSON-Dateien enthalten Inhalte."
