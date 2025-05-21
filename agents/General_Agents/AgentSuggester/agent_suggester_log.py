# agent_suggester_log.py – Logging der Agentenvorschläge

import json
import os
from datetime import datetime

LOG_PATH = "memory_logs/agent_suggestions_log.json"

def log_suggestion(data):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "suggestion": data
    }
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(LOG_PATH, "r+") as f:
            log = json.load(f)
            log.append(entry)
            f.seek(0)
            json.dump(log, f, indent=2)
