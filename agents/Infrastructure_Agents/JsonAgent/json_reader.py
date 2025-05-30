# json_reader.py – GPT-lesbare Ausgaben für JSON-Dateien

from utils.json_loader import load_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_config

# 📘 Gibt eine formatierte Vorschau des Inhalts zurück
def preview_json(file_key: str, max_entries: int = 5) -> str:
    config = get_json_config(file_key)
    if not config:
        return f"⚠️ Datei-Konfiguration für '{file_key}' nicht gefunden."

    content = load_json(config["filename"])
    if not isinstance(content, dict):
        return f"❌ Fehler beim Laden von '{file_key}': {content.get('error', 'Unbekannter Fehler')}"

    preview_lines = [f"🗂️ Vorschau: {file_key} ({config['filename']})"]
    for i, (k, v) in enumerate(content.items()):
        if i >= max_entries:
            preview_lines.append(f"... und weitere {len(content) - max_entries} Einträge")
            break
        preview_lines.append(f"– **{k}:** {str(v)[:100]}")  # ggf. kürzen

    return "\n".join(preview_lines)


# 📂 Gibt vollständige Inhalte zurück (für Debugging oder Memory)
def full_json_dump(file_key: str) -> dict:
    config = get_json_config(file_key)
    if not config:
        return {"error": f"Datei-Konfiguration für '{file_key}' nicht gefunden."}

    content = load_json(config["filename"])
    return content if isinstance(content, dict) else {"error": "Fehler beim Laden."}


# 📎 Gibt strukturierte Metadaten über eine Datei zurück
def describe_json(file_key: str) -> str:
    config = get_json_config(file_key)
    if not config:
        return f"⚠️ Keine Informationen über '{file_key}' verfügbar."

    return (
        f"📎 **Datei:** {config.get('filename')}\n"
        f"📘 **Beschreibung:** {config.get('description', '–')}\n"
        f"🏷️ **Tags:** {', '.join(config.get('tags', []))}\n"
        f"🔒 **Status:** {config.get('status', 'unbekannt')}"
    )
