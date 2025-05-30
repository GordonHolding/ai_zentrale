# json_updater.py – gezieltes Schreiben & Ersetzen von JSON-Inhalten

from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_config
from agents.Infrastructure_Agents.JsonAgent.json_formatter import format_json
from agents.Infrastructure_Agents.JsonAgent.json_protection import is_protected
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from datetime import datetime

# 🔁 Ersetze gesamten JSON-Inhalt mit neuem Dictionary (nur wenn erlaubt)
def replace_json_content(file_key, new_data: dict):
    config = get_json_config(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    if is_protected(config["filename"]):
        return f"⛔ Datei '{file_key}' ist schreibgeschützt."

    formatted_data = format_json(new_data)
    result = write_json(config["filename"], formatted_data)

    if not result.get("success"):
        return f"❌ Fehler beim Ersetzen von '{file_key}'."

    log_interaction("JsonAgent", {
        "type": "JsonReplace",
        "file": file_key,
        "content_size": len(formatted_data),
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ Inhalt von '{file_key}' wurde vollständig ersetzt."


# 🔎 Ersetze nur ein bestimmtes Schlüsselwort (immer überschreiben)
def overwrite_key(file_key, key: str, new_value):
    config = get_json_config(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    if is_protected(config["filename"]):
        return f"⛔ Datei '{file_key}' ist schreibgeschützt."

    data = load_json(config["filename"])
    if not isinstance(data, dict):
        return f"❌ Fehler beim Laden von '{file_key}': {data.get('error', 'Unbekannt')}"

    data[key] = new_value
    formatted_data = format_json(data)
    result = write_json(config["filename"], formatted_data)

    if not result.get("success"):
        return f"❌ Fehler beim Aktualisieren von '{key}' in '{file_key}'."

    log_interaction("JsonAgent", {
        "type": "JsonKeyOverwrite",
        "file": file_key,
        "key": key,
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ Schlüssel '{key}' wurde in '{file_key}' überschrieben."
