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
conversation_store: Dict[str, List[List[Dict]]] = {}

# 🗃️ Bestehende Daten laden (falls vorhanden)
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

# 🔍 Aktuellen Kontext abrufen (letzte 5 Sessions)
def get_recent_context(user_id: str = "default") -> List[Dict]:
    sessions = conversation_store.get(user_id, [])
    return [msg for session in sessions[-5:] for msg in session]

# ✏️ Neue Nachricht starten (Neue Session)
def start_new_session(user_id: str = "default"):
    conversation_store.setdefault(user_id, []).append([])
    if len(conversation_store[user_id]) > 5:
        conversation_store[user_id] = conversation_store[user_id][-5:]
    save_log()

# 💬 GPT-Antwort oder Nutzernachricht hinzufügen
def log_message(user_id: str, role: str, content: str):
    if user_id not in conversation_store or not conversation_store[user_id]:
        start_new_session(user_id)
    conversation_store[user_id][-1].append({
        "role": role,
        "content": content,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })
    save_log()

# 📎 System-Kommentar hinzufügen (z. B. Upload, Hinweis)
def log_system_note(user_id: str, note: str):
    log_message(user_id, "system", f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}")

# ♻️ Vollständiger Reset eines Users
def reset_context(user_id: str = "default"):
    conversation_store[user_id] = []
    save_log()

# 🧠 Für GPT-Auswertung alle Sessions in flacher Liste
def get_all_sessions_flat(user_id: str = "default") -> List[Dict]:
    sessions = conversation_store.get(user_id, [])
    return [msg for session in sessions for msg in session]

# 🔍 Kontext optional schlank extrahieren (Zusammenfassungen möglich)
def get_all_sessions_slim(user_id: str = "default") -> List[str]:
    sessions = conversation_store.get(user_id, [])
    return [f"{s[0]['content']} … {s[-1]['content']}" if s else "Leere Sitzung" for s in sessions]

# 💾 Zentral speichern
def save_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(conversation_store, f, indent=2, ensure_ascii=False)

# ✅ Alias für Kompatibilität mit get_context()
get_context = get_recent_context
