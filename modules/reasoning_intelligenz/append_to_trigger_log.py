# append_to_trigger_log.py

import os
import json
from datetime import datetime

LOG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/TriggerAgent_Protokolle/trigger_execution_log.json"

def append_trigger_log(trigger_name, result_text):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "trigger": trigger_name,
        "result": result_text
    }

    data = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append(entry)

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
