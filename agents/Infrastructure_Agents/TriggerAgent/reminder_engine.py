# reminder_engine.py – löst GPT-basierte Erinnerungen bei Fristen aus

from modules.reasoning_intelligenz.deadline_checker import check_deadlines
from modules.reasoning_intelligenz.memory_log import log_interaction
from datetime import datetime

def run_reminder_routine():
    warnings = check_deadlines()
    if not warnings:
        return "✅ Keine kritischen Fristen erkannt."

    log_interaction("System", {
        "type": "Reminder",
        "entries": warnings,
        "timestamp": datetime.now().isoformat()
    })

    return "🔔 Erinnerung aktiv:\n" + "\n".join(warnings)
