# context_memory.py – RAM-Level Store für JSON-Kontexte (Prompts, Registry, Index etc.)

import threading

# Interner Kontextspeicher (thread-safe)
_context_store = {}
_lock = threading.Lock()


# 🔁 Allgemeine Funktionen

def set_context(key: str, value: dict):
    """Setzt ein Kontextobjekt im Speicher."""
    with _lock:
        _context_store[key] = value


def get_context(key: str = None):
    """Liefert entweder gesamten Kontext oder den Wert eines Schlüssels."""
    with _lock:
        if key:
            return _context_store.get(key)
        return _context_store.copy()


def update_context(new_data: dict):
    """Fügt neue Schlüssel-Werte zum Kontext hinzu (oder überschreibt bestehende)."""
    with _lock:
        _context_store.update(new_data)


def get_context_value(key: str, default=None):
    """Gibt den Kontextwert für einen Schlüssel zurück, mit Fallback."""
    with _lock:
        return _context_store.get(key, default)


def clear_context():
    """Setzt den Kontextspeicher vollständig zurück."""
    with _lock:
        _context_store.clear()
        print("[CONTEXT_MEMORY] Kontext wurde zurückgesetzt.")


# 🔍 JSON-Hilfsfunktionen

def get_json(filename: str) -> dict:
    """Greift auf ein geladenes JSON im Kontext zu (z. B. 'index.json')"""
    with _lock:
        return _context_store.get(filename, {})


def get_prompt() -> dict:
    """Lädt den aktuellen Systemprompt (gpt_agent_prompt.json)"""
    prompt_path = _context_store.get("gpt_config", {}).get("PROMPT_PATH", "gpt_agent_prompt.json")
    return _context_store.get(prompt_path, {})


def get_config() -> dict:
    """Lädt die aktuelle GPT-Konfiguration"""
    return _context_store.get("gpt_config", {})


# 🧠 Für Monitoring- & Statuszwecke (RAM-Debug)

def get_all_context() -> dict:
    """Gibt den gesamten RAM-Kontext als Kopie zurück (readonly)."""
    with _lock:
        return _context_store.copy()
