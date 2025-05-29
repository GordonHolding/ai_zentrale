# context_tracker.py – Mehrfach-Speicher für lokale Kurzzeitkontexte (bis 5 Sessions)

import os
import json
import datetime
from typing import List, Dict

# 📁 Basispfade
BASE_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History"
LOG_PATH = os.path.join(BASE_DIR, "recent_context.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# ⚙️ Einstellungen
MAX_RECENT_SESSIONS = 5

# 📂 Verzeichnisse anlegen
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🧠 Kontextspeicherstruktur: user_id → Liste von Sessions → Liste von Nachrichten
context_store: Dict[str, List[List[Dict]]] = {}

# 📥 Bestehende Daten laden
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            context_store = json.load(f)
        except json.JSONDecodeError:
            context_store = {}

# 🆕 Neue Session starten
def start_new_session(user_id: str):
    context_store.setdefault(user_id, []).append([])
    # Wenn mehr als erlaubt → älteste Session löschen
    if len(context_store[user_id]) > MAX_RECENT_SESSIONS:
        context_store[user_id].pop(0)
    save_log()

# ➕ Nutzernachricht hinzufügen
def log_user_message(user_id: str, message: str):
    if user_id not in context_store or not context_store[user_id]:
        start_new_session(user_id)
    context_store[user_id][-1].append({
        "role": "user",
        "content": message
    })
    save_log()

# ➕ GPT-Antwort hinzufügen
def log_assistant_reply(user_id: str, reply: str):
    if user_id not in context_store or not context_store[user_id]:
        start_new_session(user_id)
    context_store[user_id][-1].append({
        "role": "assistant",
        "content": reply
    })
    save_log()

# 🔁 Session vollständig zurücksetzen
def reset_context(user_id: str):
    context_store[user_id] = []
    save_log()

# 📎 Datei-Kommentar hinzufügen
def attach_file_summary(user_id: str, summary: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if user_id not in context_store or not context_store[user_id]:
        start_new_session(user_id)
    context_store[user_id][-1].append({
        "role": "system",
        "content": f"📎 Datei-Upload registriert am {timestamp}: {summary}"
    })
    save_log()

# 🔍 Kontext eines Nutzers abrufen
def get_context(user_id: str) -> List[List[Dict]]:
    return context_store.get(user_id, [])

# 💾 Speichern
def save_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(context_store, f, indent=2, ensure_ascii=False)
