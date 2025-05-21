# memory_log.py

import os
import json
from datetime import datetime

DEFAULT_LOG_FILE = "0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History/memory_log.json"

def log_interaction(user, prompt, response, path=DEFAULT_LOG_FILE):
    memory = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            try:
                memory = json.load(f)
            except:
                memory = []
    memory.append({
        "type": "chat",
        "user": user,
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def log_mail_entry(mail_id, sender, subject, category, summary, path=DEFAULT_LOG_FILE):
    memory = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            try:
                memory = json.load(f)
            except:
                memory = []
    memory.append({
        "type": "mail",
        "mail_id": mail_id,
        "sender": sender,
        "subject": subject,
        "category": category,
        "summary": summary,
        "timestamp": datetime.utcnow().isoformat()
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
