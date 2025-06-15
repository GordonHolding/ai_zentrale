# context_memory.py
# RAM-basierter Zwischenspeicher für Systemkontext (Prompts, Registry, Index etc.)

import threading

_context_store = {}
_lock = threading.Lock()


def set_context(key: str, value: dict):
    """Speichert ein Kontextobjekt unter dem gegebenen Schlüssel."""
    with _lock:
        _context_store[key] = value


def get_context(key: str):
    """Liefert das Kontextobjekt für den Schlüssel oder None."""
    with _lock:
        return _context_store.get(key)


def get_all_context():
    """Gibt den gesamten Kontext (readonly) zurück."""
    with _lock:
        return _context_store.copy()


def clear_context():
    """Löscht alle gespeicherten Kontextobjekte."""
    with _lock:
        _context_store.clear()
        print("[CONTEXT_MEMORY] Kontext wurde zurückgesetzt.")
