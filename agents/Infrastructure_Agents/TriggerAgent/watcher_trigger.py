# agents/Infrastructure_Agents/TriggerAgent/watcher_trigger.py

from datetime import datetime
from utils.json_loader import load_json, write_json
from agents.General_Agents.DriveAgent.drive_utils import list_files_in_folder
from agents.General_Agents.DriveAgent.file_metadata_engine import enrich_file_metadata

WATCHED_FOLDER_ID = load_json("drive_config.json").get("watched_folder_id", "")
WATCHER_META_KEY = "watcher_trigger_log.json"
STRUCTURE_META_KEY = "file_structure_meta.json"

# ▶ Hauptscan: Findet neue Dateien, aktualisiert Metadaten, loggt Info
def scan_drive_and_trigger() -> str:
    if not WATCHED_FOLDER_ID:
        return "❌ Kein Watcher-Folder definiert."

    try:
        previous_files = load_json(WATCHER_META_KEY)
        if not isinstance(previous_files, list):
            previous_files = []
    except:
        previous_files = []

    current_files = list_files_in_folder(WATCHED_FOLDER_ID)
    new_files = []
    previous_ids = {f["id"] for f in previous_files if "id" in f}

    for f in current_files:
        if f.get("id") not in previous_ids:
            f["watcher_detected"] = True
            new_files.append(f)

    if not new_files:
        return "✅ Keine neuen Dateien erkannt."

    enriched = enrich_file_metadata(new_files)
    write_json(WATCHER_META_KEY, current_files)

    try:
        all_entries = load_json(STRUCTURE_META_KEY)
        if not isinstance(all_entries, list):
            all_entries = []
    except:
        all_entries = []

    all_entries.extend(enriched)
    write_json(STRUCTURE_META_KEY, all_entries)

    return f"🔍 {len(new_files)} Datei(en) erkannt und analysiert."

# ▶ Wrapper für Trigger-System (liefert Trigger-Objekte zurück)
def check_watcher_trigger(config: dict) -> list:
    if not WATCHED_FOLDER_ID:
        return []
    return [{
        "type": "watcher_trigger",
        "name": "scan_drive_structure",
        "source": "watcher_check",
        "timestamp": datetime.utcnow().isoformat()
    }]

# ▶ Optional: Direktes Testen
if __name__ == "__main__":
    result = scan_drive_and_trigger()
    print(result)
