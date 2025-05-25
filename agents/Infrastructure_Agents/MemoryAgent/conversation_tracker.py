# conversation_tracker.py – File Handling für GPT-Verlauf

import os
import json
import datetime
from typing import List, Dict

# ⚠️ Universeller Pfad für GDrive & Render
BASE_DIR = "chat_history"
LOG_PATH = os.path.join(BASE_DIR, "chat_history_log.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# Verzeichnisse anlegen
os.makedirs(UPLOAD_DIR, exist_ok=True)

conversation_store: Dict[str, List[Dict]] = {}

if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

def get_context(user_id: str) -> List[Dict]:
    return conversation_store.get(user_id, [])

def log_and_get_context(user_id: str, message: str) -> List[Dict]:
    conversation_store.setdefault(user_id, []).append({"role": "user", "content": message})
    save_log()
    return conversation_store[user_id]

def add_gpt_reply(user_id: str, reply: str):
    conversation_store.setdefault(user_id, []).append({"role": "assistant", "content": reply})
    save_log()

def reset_context(user_id: str):
    conversation_store[user_id] = []
    save_log()

def attach_file_summary(user_id: str, summary: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conversation_store.setdefault(user_id, []).append({
        "role": "system",
        "content": f"📎 Datei-Upload registriert am {timestamp}: {summary}"
    })
    save_log()

def save_log():
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(conversation_store, f, indent=2)
