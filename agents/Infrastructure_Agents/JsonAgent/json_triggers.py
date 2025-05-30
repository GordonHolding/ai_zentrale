# json_triggers.py – Triggerlogik für JsonAgent

import datetime
from agents.Infrastructure_Agents.JsonAgent import json_agent
from agents.Infrastructure_Agents.MemoryAgent import memory_log
from agents.Infrastructure_Agents.JsonAgent.json_validator import validate_entry

# 📌 Trigger bei Systemstart
def trigger_on_startup():
    timestamp = datetime.datetime.now().isoformat()
    memory_log.log_system_start(entries=[
        f"[JsonAgent] Initialisiert um {timestamp}",
        "Trigger: trigger_on_startup()",
        "Status: Bereit zur Analyse von JSON-Dateien"
    ])
    print("✅ JsonAgent bereit (Startup Trigger)")

# 📂 Trigger bei neuer JSON-Datei im System (z. B. via Watcher)
def trigger_on_new_json(file_path: str):
    try:
        result = json_agent.analyze_json(file_path)
        log_routing(file_path, result)
        return result
    except Exception as e:
        memory_log.log_mail_entry(
            mail_id="JSON-TRIGGER-ERROR",
            sender="system",
            subject="JsonAgent Trigger Error",
            category="trigger",
            summary=str(e)
        )
        return f"[Fehler im JsonAgent Trigger]: {str(e)}"

# 🧾 Routing-Log schreiben (über MemoryAgent)
def log_routing(file_path, result):
    memory_log.log_interaction("JsonAgent", "📦 JSON-Datei analysiert", {
        "file": file_path,
        "output_preview": str(result)[:100],
        "timestamp": datetime.datetime.now().isoformat()
    })
