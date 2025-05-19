# json_agent.py – zentrale Logik für GPT-gesteuerte JSON-Verwaltung

from agents.Infrastructure_Agents.JsonAgent.json_utils import load_json, write_json
from agents.Infrastructure_Agents.JsonAgent.json_config import JSON_CONFIG_LIST
from datetime import datetime
from modules.reasoning_intelligenz.memory_log import log_interaction

def update_json_entry(file_key, key, value, overwrite=False):
    config = JSON_CONFIG_LIST.get(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    path = config["path"]
    data = load_json(path)

    if not overwrite and key in data:
        return f"⚠️ Schlüssel '{key}' existiert bereits in '{file_key}'."

    data[key] = value
    write_json(path, data)

    log_interaction("System", {
        "type": "JsonUpdate",
        "file": file_key,
        "key": key,
        "value": str(value),
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ '{key}' wurde in '{file_key}' aktualisiert."
