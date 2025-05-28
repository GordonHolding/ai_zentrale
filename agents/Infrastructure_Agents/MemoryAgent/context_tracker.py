# context_tracker.py – Lokale Chat-Session für User-Verlauf, Uploads & Kontexte

import os
import json
import datetime
from typing import List, Dict

# 🔁 Basispfad für Konversationen
BASE_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History"
LOG_PATH = os.path.join(BASE_DIR, "recent_context.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# 📁 Verzeichnisse sicherstellen
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(BASE_DIR, exist_ok=True)

# 🧠 Interner Speicher (Speichert Verlauf pro Nutzer)
conversation_store: Dict[str, List[Dict]] = {}

# 🗃️ Lade bestehende Daten (falls vorhanden)
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

# 🔍 Aktuellen Kontext eines Users abrufen
def get_context(user_id: str) -> List[Dict]:
    return conversation_store.get(user_id, [])

# ✏️ Neuen Nutzereintrag hinzufügen + speichern
def log_and_get_context(user_id: str, message: str) -> List[Dict]:
    conversation_store.setdefault(user_id, []).append({
        "role": "user",
        "content": message
    })
    save_log()
    return conversation_store[user_id]

# 💬 GPT-Antwort anhängen
def add_gpt_reply(user_id: str, reply: str):
    conversation_store.setdefault(user_id, []).append({
        "role": "assistant",
        "content": reply
    })
    save_log()

# ♻️ Kontext für einen User zurücksetzen
def reset_context(user_id: str):
    conversation_store[user_id] = []
    save_log()

# 📎 Kommentar für Datei-Upload speichern
def attach_file_summary(user_id: str, summary: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conversation_store.setdefault(user_id, []).append({
        "role": "system",
        "content": f"📎 Datei-Upload registriert am {timestamp}: {summary}"
    })
    save_log()

# 💾 Lokal speichern
def save_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(conversation_store, f, indent=2, ensure_ascii=False)

# 🔄 Für Kontextabruf über context_manager
def get_recent_context():
    return conversation_store
