# conversation_tracker.py – Dauerhafte GPT-Verlaufsstruktur mit Memory-Erweiterung

import os
import json
import datetime
from typing import List, Dict

# 🔁 Globale Dateiablage
BASE_DIR = "chat_history"
LOG_PATH = os.path.join(BASE_DIR, "chat_history_log.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")

# 📁 Sicherstellen, dass Ordner existieren
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🧠 Internes Speicherobjekt – strukturierter Verlauf für GPT-Kompatibilität
conversation_store: Dict[str, List[Dict]] = {}

# 🗃️ Lade bestehenden Verlauf aus Datei (falls vorhanden)
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            conversation_store = json.load(f)
        except json.JSONDecodeError:
            conversation_store = {}

# 🔎 Holt vollständigen GPT-Verlauf eines Nutzers
def get_conversation(user_id: str) -> List[Dict]:
    return conversation_store.get(user_id, [])

# ✏️ Neuen Nutzereintrag protokollieren
def log_user_message(user_id: str, message: str):
    conversation_store.setdefault(user_id, []).append({
        "role": "user",
        "content": message
    })
    save_log()

# 💬 Antwort von GPT ergänzen
def log_assistant_reply(user_id: str, reply: str):
    conversation_store.setdefault(user_id, []).append({
        "role": "assistant",
        "content": reply
    })
    save_log()

# 🔁 Kontext zurücksetzen für neue GPT-Sessions
def reset_conversation(user_id: str):
    conversation_store[user_id] = []
    save_log()

# 📎 Datei-Kommentare von GPT oder Nutzer
def log_system_note(user_id: str, note: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conversation_store.setdefault(user_id, []).append({
        "role": "system",
        "content": f"[{timestamp}] {note}"
    })
    save_log()

# 💾 Zentrale Speicherfunktion
def save_log():
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(conversation_store, f, indent=2, ensure_ascii=False)

# 🔄 Für Kontextabruf über context_manager
def get_conversation_context() -> Dict[str, List[Dict]]:
    return conversation_store
