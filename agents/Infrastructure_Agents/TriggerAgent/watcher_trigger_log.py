# watcher_trigger_log.py

import os
import json
from datetime import datetime
from utils.json_loader import load_json, write_json

LOG_PATH = "0.2 Agenten/Infrastructure_Agents/TriggerAgent/TriggerAgent_Protokolle/watcher_trigger_log.json"


def append_watcher_log(change_type: str, file_info: dict, trigger_source: str = "WatcherTrigger"):
    """
    Protokolliert Änderungen am Dateisystem in einer systemischen Logdatei.
    
    Args:
        change_type (str): Typ der Änderung, z. B. "new_file", "moved_file", "deleted_file"
        file_info (dict): GPT-relevante Informationen zur Datei (Pfad, Name, Typ etc.)
        trigger_source (str): Name des auslösenden Moduls oder Agenten (Standard: "WatcherTrigger")
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "change_type": change_type,
        "file": file_info,
        "trigger_source": trigger_source
    }

    # Bestehende Logs laden
    logs = []
    if os.path.exists(LOG_PATH):
        try:
            logs = load_json(LOG_PATH)
        except:
            logs = []

    logs.append(log_entry)

    # Speichern
    write_json(LOG_PATH, logs)
