# context_manager.py – Zentrale Kontextsteuerung & Caching

import os
import json
from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.context_tracker import get_context as get_context_sessions
from agents.Infrastructure_Agents.MemoryAgent.conversation_tracker import get_conversation_context
from agents.Infrastructure_Agents.MemoryAgent.memory_log import get_memory_log

# 🔁 Cache-Speicher für bereits geladene Kontexte
_context_cache = {}

# 🔑 Pfaddefinitionen für zentrale JSON-Dateien
_JSON_PATHS = {
    "identity": "system_identity_prompt.json",
    "index": "index.json",
    "agents": "agent_registry.json",
    "drive_config": "0.3 AI-Regelwerk & Historie/Systemregeln/Config/drive_index_config.json",
    "chat_history_log": "system_logs/chat_history_log.json",  # NEU: Read-only Kontext
}

# ✅ Kontext abrufen mit intelligentem Cache
def get_context(name, user_id="default"):
    if name in _context_cache:
        return _context_cache[name]

    if name == "recent_chat":
        sessions = get_context_sessions(user_id)
        data = sessions[-1] if sessions else []  # Liefert nur die aktuellste Session
    elif name == "conversation":
        data = get_conversation_context().get(user_id, [])
    elif name == "memory_log":
        data = get_memory_log()
    elif name == "chat_history_log":
        data = _load_json_file(_JSON_PATHS["chat_history_log"])  # expliziter Read-only-Zugriff
    elif name == "projects":
        # ✅ Statt structure_content_loader jetzt direkte Auslesung des Verzeichnisses
        path = "0.3 AI-Regelwerk & Historie/Systemregeln/Projekte"
        data = []
        for fname in os.listdir(path):
            if fname.endswith(".json"):
                fpath = os.path.join(path, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    data.append(json.load(f))
    else:
        file_path = _JSON_PATHS.get(name)
        if not file_path:
            raise ValueError(f"Unbekannter Kontext: {name}")
        data = load_json(file_path)

    _context_cache[name] = data
    return data

# ▶️ Alles auf einmal laden (für startup_loader)
def preload_all():
    for key in _JSON_PATHS:
        get_context(key)
    get_context("recent_chat")
    get_context("conversation")
    get_context("memory_log")

# ❌ Cache zurücksetzen (z. B. bei Reload)
def clear_context_cache():
    _context_cache.clear()

# 🔐 Interne Utility-Funktion für direkten JSON-Read
def _load_json_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
