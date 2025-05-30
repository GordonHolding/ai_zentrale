# json_log_writer.py – Änderungsprotokoll für JSON-Eingriffe inkl. Memory-Verknüpfung

import datetime
from agents.Infrastructure_Agents.MemoryAgent import memory_log
from utils.json_loader import load_json, write_json

# 📓 Log-Datei für JSON-Vorgänge (Pfad über Systemindex steuerbar)
JSON_LOG_FILENAME = "json_change_log.json"

# 📌 Strukturierter Log-Eintrag für jede JSON-Änderung
def log_json_change(file_key, key, action_type, new_value=None, old_value=None):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "file": file_key,
        "key": key,
        "action": action_type,
        "new_value": new_value,
        "old_value": old_value
    }

    # 🔁 Bestehendes Log laden und erweitern
    log_data = load_json(JSON_LOG_FILENAME)
    if isinstance(log_data, dict) and "logs" in log_data:
        log_data["logs"].append(log_entry)
    else:
        log_data = {"logs": [log_entry]}

    write_json(JSON_LOG_FILENAME, log_data)

    # 🧠 Optional: MemoryAgent informieren bei kritischer Änderung
    if action_type in ["replace", "overwrite", "delete"]:
        memory_log.log_entry({
            "source": "JsonAgent",
            "category": "json_change",
            "summary": f"Änderung in {file_key}: [{key}] wurde {action_type}",
            "details": log_entry
        })

    return f"📘 Änderung geloggt: {file_key} – [{key}] – {action_type}"
