# context_manager.py – Zentrale Kontextsteuerung & Caching

import os
import json
from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.context_tracker import get_recent_context
from agents.Infrastructure_Agents.MemoryAgent.conversation_tracker import get_conversation_context
from agents.Infrastructure_Agents.MemoryAgent.memory_log import get_memory_log

# 🔁 Cache-Speicher für bereits geladene Kontexte
_context_cache = {}

# 🔑 Pfaddefinitionen für zentrale JSON-Dateien
_JSON_PATHS = {
    "identity": "system_identity_prompt.json",
    "index": "index.json",
    "agents": "agent_registry.json",
    "projects": "structure_content_loader",  # ❌ wird gleich ersetzt
    "drive_config": "0.3 AI-Regelwerk & Historie/Systemregeln/Config/drive_index_config.json"
}

# ✅ Kontext abrufen mit intelligentem Cache
def get_context(name):
    if name in _context_cache:
        return _context_cache[name]

    if name == "recent_chat":
        data = get_recent_context()
    elif name == "conversation":
        data = get_conversation_context()
    elif name == "memory_log":
        data = get_memory_log()
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

# ▶þ Alles auf einmal laden (für startup_loader)
def preload_all():
    for key in _JSON_PATHS:
        get_context(key)
    get_context("recent_chat")
    get_context("conversation")
    get_context("memory_log")

# ❌ Cache zurücksetzen (z. B. bei Reload)
def clear_context_cache():
    _context_cache.clear()
