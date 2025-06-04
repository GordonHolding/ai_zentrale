# watcher_trigger.py – erkennt neue Dateien im Drive-Folder und prüft Trigger-Konfiguration

from datetime import datetime
from utils.json_loader import load_json, write_json
from agents.General_Agents.DriveAgent.drive_utils import list_files_in_folder
from agents.General_Agents.DriveAgent.file_metadata_engine import enrich_file_metadata
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_trigger_execution

WATCHED_FOLDER_ID = load_json("drive_config.json").get("watched_folder_id", "")
WATCHER_META_KEY = "watcher_trigger_log.json"
STRUCTURE_META_KEY = "file_structure_meta.json"

# 🔍 Erkennt neue Dateien und führt Metadatenanalyse durch
def scan_drive_and_trigger():
    if not WATCHED_FOLDER_ID:
        return "❌ Kein Watcher-Folder definiert."

    try:
        previous_files = load_json(WATCHER_META_KEY)
    except:
        previous_files = []

    current_files = list_files_in_folder(WATCHED_FOLDER_ID)
    new_files = []
    previous_ids = {f["id"] for f in previous_files}

    for f in current_files:
        if f["id"] not in previous_ids:
            f["watcher_detected"] = True
            new_files.append(f)

    if not new_files:
        return "✅ Keine neuen Dateien erkannt."

    enriched = enrich_file_metadata(new_files)
    write_json(WATCHER_META_KEY, current_files)

    try:
        all_entries = load_json(STRUCTURE_META_KEY)
    except:
        all_entries = []

    all_entries.extend(enriched)
    write_json(STRUCTURE_META_KEY, all_entries)

    log_trigger_execution("WatcherTrigger", [f["name"] for f in new_files], datetime.now().isoformat())
    return f"🔍 {len(new_files)} Datei(en) erkannt und analysiert."

# ✅ Ergänzt: Liefert aktive Watcher-Trigger aus Konfig zurück
def check_watcher_trigger(config: dict) -> list:
    results = []
    for trig in config.get("watcher_triggers", []):
        if not trig.get("enabled", True):
            continue
        results.append({
            "type": "watcher_trigger",
            "name": trig.get("name", "unnamed_watcher_trigger"),
            "source": "watcher_config",
            "timestamp": datetime.utcnow().isoformat()
        })
    return results
