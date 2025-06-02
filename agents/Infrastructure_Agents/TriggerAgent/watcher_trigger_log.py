# watcher_trigger_log.py – Logging aller strukturellen Änderungen

import json
from datetime import datetime

TRIGGER_LOG_PATH = "memory_logs/watcher_trigger_log.json"

def log_trigger_event(entries):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "new_structure_elements": entries
    }
    try:
        with open(TRIGGER_LOG_PATH, "r+") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open(TRIGGER_LOG_PATH, "w") as f:
            json.dump([log_entry], f, indent=2)
