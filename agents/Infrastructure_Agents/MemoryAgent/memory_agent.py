# memory_log.py – Logging-Funktionen für AI-Zentrale (Chat, Mail, Systemstart)

import os
import json
from datetime import datetime
from utils.json_loader import get_json_by_keyword

# 📁 Hole Log-Dateipfad dynamisch via JSON
DEFAULT_LOG_FILE = get_json_by_keyword("memory_config").get("MEMORY_LOG_PATH", "MemoryAgent/MemoryAgent_Memory/memory_log.json")

# 🧠 Chat-Verlauf loggen
def log_interaction(user, prompt, response, path=DEFAULT_LOG_FILE):
    memory = load_log(path)
    memory.append({
        "type": "chat",
        "user": user,
        "prompt": prompt,
        "response": response,
        "timestamp": timestamp()
    })
    save_log(memory, path)

# 📧 Mail-Eintrag loggen
def log_mail_entry(mail_id, sender, subject, category, summary, path=DEFAULT_LOG_FILE):
    memory = load_log(path)
    memory.append({
        "type": "mail",
        "mail_id": mail_id,
        "sender": sender,
        "subject": subject,
        "category": category,
        "summary": summary,
        "timestamp": timestamp()
    })
    save_log(memory, path)

# 🚀 Systemstart-Eintrag loggen (wird von startup_loader.py verwendet)
def log_system_start(path=DEFAULT_LOG_FILE, entries=None):
    if entries is None:
        entries = []
    memory = load_log(path)
    memory.append({
        "type": "system_start",
        "entries": entries,
        "timestamp": timestamp()
    })
    save_log(memory, path)

# 📂 Bestehende Logs laden
def load_log(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

# 💾 Logs speichern
def save_log(memory, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

# 🕒 Zeitstempel
def timestamp():
    return datetime.utcnow().isoformat()

# 🔄 Für Kontextabruf über context_manager
def get_memory_log():
    return load_log(DEFAULT_LOG_FILE)
