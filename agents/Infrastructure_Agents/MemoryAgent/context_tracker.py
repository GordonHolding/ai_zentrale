# context_tracker.py – Kurzzeitgedächtnis mit Session-Struktur (max. 5 Sessions)

import os
import json
import datetime
from typing import List, Dict

# 📁 Basispfade
BASE_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History"
LOG_PATH = os.path.join(BASE_DIR, "recent_context.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# 📁 Sicherstellen, dass Ordner existieren
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(BASE_DIR, exist_ok=True)

# 🧠 Speicherstruktur: user_id → List of Sessions → List of Messages
# Eine Session = List[Dict]
conversation_store: Dict[str, List[List[Dict]]] = {}

# 🗃️ Lade bestehende Kontexte
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

# ✅ Hilfsfunktion: Speichern
def save_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(conversation_store, f, indent=2, ensure_ascii=False)

# 🔁 Starte neue Session für Nutzer
def start_new_session(user_id: str):
    conversation_store.setdefault(user_id, []).append([])

    # Maximal 5 Sessions behalten
    if len(conversation_store[user_id]) > 5:
        conversation_store[user_id].pop(0)

    save_log()

# ✏️ Nachricht des Nutzers hinzufügen
def log_and_get_context(user_id: str, message: str) -> List[List[Dict]]:
    if user_id not in conversation_store or not conversation_store[user_id]:
        start_new_session(user_id)

    conversation_store[user_id][-1].append({
        "role": "user",
        "content": message
    })
    save_log()
    return conversation_store[user_id]

# 💬 GPT-Antwort hinzufügen
def add_gpt_reply(user_id: str, reply: str):
    if user_id not in conversation_store or not conversation_store[user_id]:
        start_new_session(user_id)

    conversation_store[user_id][-1].append({
        "role": "assistant",
        "content": reply
    })
    save_log()

# ♻️ Kontext manuell zurücksetzen (alle Sessions)
def reset_context(user_id: str):
    conversation_store[user_id] = []
    save_log()

# 📎 Kommentar zu Datei-Upload hinzufügen
def attach_file_summary(user_id: str, summary: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if user_id not in conversation_store or not conversation_store[user_id]:
        start_new_session(user_id)

    conversation_store[user_id][-1].append({
        "role": "system",
        "content": f"📎 Datei-Upload registriert am {timestamp}: {summary}"
    })
    save_log()

# 🔎 Kontext vollständig abrufen
def get_recent_context(user_id: str = "default") -> List[List[Dict]]:
    return conversation_store.get(user_id, [])
