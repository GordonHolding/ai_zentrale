# json_agent.py – zentrale Logik für GPT-gesteuerte JSON-Verwaltung

from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_config
from datetime import datetime
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# 🔁 Aktualisiert oder ergänzt einen JSON-Schlüssel
def update_json_entry(file_key, key, value, overwrite=False):
    config = get_json_config(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    data = load_json(config["filename"])
    if not isinstance(data, dict):
        return f"❌ Fehler beim Laden der Datei '{file_key}': {data.get('error', 'Unbekannter Fehler')}"

    if not overwrite and key in data:
        return f"⚠️ Schlüssel '{key}' existiert bereits in '{file_key}'."

    data[key] = value
    success = write_json(config["filename"], data)
    if not success:
        return f"❌ Schreiben in Datei '{file_key}' fehlgeschlagen."

    log_interaction("System", {
        "type": "JsonUpdate",
        "file": file_key,
        "key": key,
        "value": str(value),
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ '{key}' wurde in '{file_key}' aktualisiert."


# ▶ Beispielhafte Initialisierung
def main():
    print("✅ JSON Agent initialisiert.")
