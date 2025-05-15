# conversation_tracker.py
import time
from collections import defaultdict

# Temporärer In-Memory-Store (für Produktion später Redis oder DB)
conversation_store = defaultdict(list)

# Konfigurierbare Limits
MAX_CONTEXT_LENGTH = 20  # Anzahl Nachrichten, die zurückgegeben werden (inkl. GPT-Antworten)
MAX_CONTEXT_AGE_SECONDS = 60 * 60  # 1 Stunde

def _current_time():
    return int(time.time())

def track_message(user_id: str, role: str, content: str):
    conversation_store[user_id].append({
        "role": role,
        "content": content,
        "timestamp": _current_time()
    })

def get_context(user_id: str):
    now = _current_time()
    history = conversation_store.get(user_id, [])
    # Nur relevante Nachrichten der letzten Stunde behalten
    recent = [m for m in history if now - m["timestamp"] <= MAX_CONTEXT_AGE_SECONDS]
    return recent[-MAX_CONTEXT_LENGTH:]  # maximal X Messages zurückgeben

def reset_context(user_id: str):
    if user_id in conversation_store:
        del conversation_store[user_id]

def log_and_get_context(user_id: str, new_user_message: str):
    track_message(user_id, "user", new_user_message)
    return get_context(user_id)

def add_gpt_reply(user_id: str, reply: str):
    track_message(user_id, "assistant", reply)

# Erweiterung für Datei-Uploads (PDF, Image, etc.)
def attach_file_summary(user_id: str, summary: str):
    track_message(user_id, "user", f"[Datei-Upload] {summary}")
