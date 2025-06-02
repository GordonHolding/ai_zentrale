-----------------------------------------------------------------------------------------------------
# watcher_trigger.py

from agents.General_Agents.DriveAgent.drive_utils import list_files_in_folder
from agents.General_Agents.DriveAgent.file_metadata_engine import enrich_file_metadata
from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_execution
import os
from datetime import datetime

# Zentrale Pfade
WATCHED_FOLDER_ID = load_json("drive_config.json").get("watched_folder_id", "")
META_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/WatcherTrigger/watcher_trigger_log.json"
STRUCTURE_META_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Drive/file_structure_meta.json"

def scan_drive_and_trigger():
    if not WATCHED_FOLDER_ID:
        return "❌ Kein Watcher-Folder definiert."

    # Lade vorherige Struktur (falls vorhanden)
    previous_files = []
    if os.path.exists(META_PATH):
        try:
            previous_files = load_json("watcher_trigger_log.json")
        except:
            pass

    # Aktueller Scan
    current_files = list_files_in_folder(WATCHED_FOLDER_ID)
    new_files = []

    previous_ids = {f["id"] for f in previous_files}
    for f in current_files:
        if f["id"] not in previous_ids:
            f["watcher_detected"] = True
            new_files.append(f)

    # Keine neuen Dateien
    if not new_files:
        return "✅ Keine neuen Dateien erkannt."

    # Metadaten anreichern
    enriched = enrich_file_metadata(new_files)

    # Alte Struktur aktualisieren
    write_json("watcher_trigger_log.json", current_files)

    # Struktur-Metadatenbank erweitern
    all_entries = []
    if os.path.exists(STRUCTURE_META_PATH):
        all_entries = load_json("file_structure_meta.json")
    all_entries.extend(enriched)
    write_json("file_structure_meta.json", all_entries)

    # Logging
    log_execution("WatcherTrigger", f"{len(new_files)} neue Datei(en) erkannt und angereichert.")

    return f"🔍 {len(new_files)} Datei(en) erkannt und analysiert."
