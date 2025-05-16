import os
import json
import datetime
from typing import List, Dict

# BASISPFAD zur Ablage
BASE_DIR = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History"
LOG_PATH = os.path.join(BASE_DIR, "chat_history_log.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# Sicherstellen, dass Ordner existieren
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Interner Speicher (z. B. als RAM-Store oder Mini-Cache)
conversation_store: Dict[str, List[Dict]] = {}

# Laden vorhandener History
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

# Verlauf holen
def get_context(user_id: str) -> List[Dict]:
    return conversation_store.get(user_id, [])

# Neue Nachricht + Verlauf zurückgeben
def log_and_get_context(user_id: str, message: str) -> List[Dict]:
    conversation_store.setdefault(user_id, []).append({"role": "user", "content": message})
    save_log()
    return conversation_store[user_id]

# GPT-Antwort speichern
def add_gpt_reply(user_id: str, reply: str):
    conversation_store.setdefault(user_id, []).append({"role": "assistant", "content": reply})
    save_log()

# Kontext löschen
def reset_context(user_id: str):
    conversation_store[user_id] = []
    save_log()

# Dateiupload verlinken
def attach_file_summary(user_id: str, summary: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conversation_store.setdefault(user_id, []).append({
        "role": "system",
        "content": f"📎 Datei-Upload registriert am {timestamp}: {summary}"
    })
    save_log()

# Zentrale Speicherung als JSON-Protokoll
def save_log():
    with open(LOG_PATH, "w") as f:
        json.dump(conversation_store, f, indent=2)
