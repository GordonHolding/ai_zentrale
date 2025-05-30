# json_agent.py – zentrale Logik für GPT-gesteuerte JSON-Verwaltung

from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_config
from agents.Infrastructure_Agents.JsonAgent.json_formatter import format_json
from agents.Infrastructure_Agents.JsonAgent.json_validator import validate_entry
from agents.Infrastructure_Agents.JsonAgent.json_protection import is_protected
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from datetime import datetime

# 🔁 Aktualisiert oder ergänzt einen JSON-Schlüssel
def update_json_entry(file_key, key, value, overwrite=False):
    config = get_json_config(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    if is_protected(config["filename"]):
        return f"⛔ Datei '{file_key}' ist schreibgeschützt."

    data = load_json(config["filename"])
    if not isinstance(data, dict):
        return f"❌ Fehler beim Laden der Datei '{file_key}': {data.get('error', 'Unbekannter Fehler')}"

    if not overwrite and key in data:
        return f"⚠️ Schlüssel '{key}' existiert bereits in '{file_key}'."

    validation_result = validate_entry(key, value)
    if not validation_result.get("valid", False):
        return f"🛑 Validierungsfehler: {validation_result.get('reason', 'Unbekannt')}"

    data[key] = value
    formatted_data = format_json(data)

    success = write_json(config["filename"], formatted_data)
    if not success.get("success"):
        return f"❌ Schreiben in Datei '{file_key}' fehlgeschlagen."

    log_interaction("JsonAgent", {
        "type": "JsonUpdate",
        "file": file_key,
        "key": key,
        "value": str(value),
        "validated": True,
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ Schlüssel '{key}' wurde erfolgreich in '{file_key}' aktualisiert."


# ▶ Initialisierungs-Check
def main():
    print("✅ JsonAgent aktiviert – bereit für strukturierte JSON-Steuerung.")
