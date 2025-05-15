import json
import os
from datetime import datetime

LOG_FILE = "memory_log.json"

def log_interaction(user, prompt, response):
    memory = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            memory = json.load(f)
    memory.append({
        "type": "chat",
        "user": user,
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    })
    with open(LOG_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def log_mail_entry(mail_id, sender, subject, category, summary):
    """
    Erweitert das Memory-Log um strukturierte E-Mail-Einträge.
    """
    memory = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            memory = json.load(f)
    memory.append({
        "type": "mail",
        "mail_id": mail_id,
        "sender": sender,
        "subject": subject,
        "category": category,
        "summary": summary,
        "timestamp": datetime.utcnow().isoformat()
    })
    with open(LOG_FILE, "w") as f:
        json.dump(memory, f, indent=2)
