# watcher_trigger.py – erkennt neue Dateien im Drive-Folder

from agents.General_Agents.DriveAgent.drive_utils import list_files_in_folder
from agents.General_Agents.DriveAgent.file_metadata_engine import enrich_file_metadata
from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_trigger_execution
from datetime import datetime
import os

# 📁 BASE_DIR für Pfadstabilität
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📁 Konfiguration & Metapfade (relativ zur Projektstruktur)
WATCHED_FOLDER_ID = load_json("drive_config.json").get("watched_folder_id", "")
META_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../../../../../0.3 AI-Regelwerk & Historie/Systemregeln/WatcherTrigger/watcher_trigger_log.json"))
STRUCTURE_META_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../../../../../0.3 AI-Regelwerk & Historie/Systemregeln/Drive/file_structure_meta.json"))

def scan_drive_and_trigger():
    if not WATCHED_FOLDER_ID:
        return "❌ Kein Watcher-Folder definiert."

    # 🧠 Vorherige Dateien laden
    previous_files = []
    if os.path.exists(META_PATH):
        try:
            previous_files = load_json(META_PATH)
        except:
            pass

    # 📥 Aktuelle Dateien abrufen
    current_files = list_files_in_folder(WATCHED_FOLDER_ID)
    new_files = []
    previous_ids = {f["id"] for f in previous_files}

    for f in current_files:
        if f["id"] not in previous_ids:
            f["watcher_detected"] = True
            new_files.append(f)

    if not new_files:
        return "✅ Keine neuen Dateien erkannt."

    # 🧠 Metadaten anreichern
    enriched = enrich_file_metadata(new_files)

    # 📝 Update: Watcher-Metadaten speichern
    write_json(META_PATH, current_files)

    # 🧠 Struktur-Metadaten anhängen
    all_entries = []
    if os.path.exists(STRUCTURE_META_PATH):
        all_entries = load_json(STRUCTURE_META_PATH)
    all_entries.extend(enriched)
    write_json(STRUCTURE_META_PATH, all_entries)

    # 🪵 Logging mit vollständigen Parametern
    timestamp = datetime.now().isoformat()
    triggered_file_names = [f["name"] for f in new_files]
    log_trigger_execution("WatcherTrigger", triggered_file_names, timestamp)

    return f"🔍 {len(new_files)} Datei(en) erkannt und analysiert."
