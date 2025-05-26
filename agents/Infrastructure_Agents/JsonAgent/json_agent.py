# json_agent.py – zentrale Logik für GPT-gesteuerte JSON-Verwaltung

from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.JsonAgent.json_config import JSON_CONFIG_LIST
from datetime import datetime
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# ✅ Wert in JSON-Datei einfügen oder überschreiben
def update_json_entry(file_key, key, value, overwrite=False):
    config = JSON_CONFIG_LIST.get(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    data = load_json(config["filename"])
    if not overwrite and key in data:
        return f"⚠️ Schlüssel '{key}' existiert bereits in '{file_key}'."

    data[key] = value
    write_json(config["filename"], data)

    log_interaction("System", {
        "type": "JsonUpdate",
        "file": file_key,
        "key": key,
        "value": str(value),
        "timestamp": datetime.now().isoformat()
    })

    return f"✅ '{key}' wurde in '{file_key}' aktualisiert."


# 📖 Einzelnen Wert aus JSON-Datei lesen
def read_json_entry(file_key, key):
    config = JSON_CONFIG_LIST.get(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    data = load_json(config["filename"])
    if key not in data:
        return f"⚠️ Schlüssel '{key}' ist in '{file_key}' nicht vorhanden."

    log_interaction("System", {
        "type": "JsonRead",
        "file": file_key,
        "key": key,
        "timestamp": datetime.now().isoformat()
    })

    return data[key]


# 🗑️ Schlüssel aus JSON-Datei löschen
def delete_json_entry(file_key, key):
    config = JSON_CONFIG_LIST.get(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    data = load_json(config["filename"])
    if key not in data:
        return f"⚠️ Schlüssel '{key}' ist in '{file_key}' nicht vorhanden."

    del data[key]
    write_json(config["filename"], data)

    log_interaction("System", {
        "type": "JsonDelete",
        "file": file_key,
        "key": key,
        "timestamp": datetime.now().isoformat()
    })

    return f"🗑️ Schlüssel '{key}' wurde aus '{file_key}' entfernt."


# 📋 Alle Schlüssel in der JSON-Datei auflisten
def list_json_keys(file_key):
    config = JSON_CONFIG_LIST.get(file_key)
    if not config:
        return f"❌ Datei-Konfiguration für '{file_key}' nicht gefunden."

    data = load_json(config["filename"])
    keys = list(data.keys())

    log_interaction("System", {
        "type": "JsonKeyList",
        "file": file_key,
        "key_count": len(keys),
        "timestamp": datetime.now().isoformat()
    })

    return keys


# ▶ Beispielhafte Initialisierung
def main():
    print("✅ JSON Agent initialisiert.")
