# systemguardian_triggers.py

import json
from datetime import datetime
from modules.reasoning_intelligenz.append_to_trigger_log import append_trigger_log
from modules.output_infrastruktur.mail_tools import send_mail
from .systemguardian_config import LOG_PATHS

def escalate_security_incident(message: str):
    """
    Wird ausgelöst, wenn z. B. ein unautorisierter Zugriff erkannt wurde.
    """
    timestamp = datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "message": message,
        "level": "high",
        "triggered_by": "SystemGuardian"
    }

    try:
        with open(LOG_PATHS["security"], "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except:
        with open(LOG_PATHS["security"], "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2)

    send_mail(
        recipient="barry@gordonholding.de",
        subject="🚨 Sicherheitsmeldung der AI-Zentrale",
        message_text=message,
        mail_mode="save_draft_confirm"
    )

    append_trigger_log("SystemGuardian_Eskalation", f"⚠️ Sicherheitsmeldung registriert: {message}")
