# agents.GPTAgent.context_manager.py

from utils.json_loader import load_json

# Hilfsfunktion für robustes JSON-Laden mit Fehlerprüfung
def checked_load_json(filename, context_hint):
    data = load_json(filename)
    if not isinstance(data, dict) or ""error"" in data:
        raise RuntimeError(
            f""Fehler beim Laden von '{context_hint}': {data.get('error') if isinstance(data, dict) else 'Unbekannter Fehler'}""
        )
    return data

# MemoryAgent-Module optional importieren (robust gegen Deaktivierung)
try:
    from agents.Infrastructure_Agents.MemoryAgent.context_tracker import get_context as get_context_sessions
    from agents.Infrastructure_Agents.MemoryAgent.conversation_tracker import get_conversation_context
    from agents.Infrastructure_Agents.MemoryAgent.memory_log import get_memory_log
except ImportError:
    def get_context_sessions():
        return None
    def get_conversation_context():
        return None
    def get_memory_log():
        return None

# Lade zentrale GPT-Konfiguration
CONFIG = checked_load_json(""gpt_config.json"", ""gpt_config.json"")

# Konfigurationspfade aus gpt_config.json
SYSTEM_IDENTITY_PATH = CONFIG.get(
    ""SYSTEM_IDENTITY_PATH"",
    ""0.3 AI-Regelwerk & Historie/AI-Zentrale_Struktur & Identität/system_identity_prompt.json""
)
INDEX_PATH = CONFIG.get(
    ""INDEX_PATH"",
    ""0.3 AI-Regelwerk & Historie/AI-Zentrale_Struktur & Identität/index.json""
)
MEMORY_INDEX_PATH = CONFIG.get(
    ""MEMORY_INDEX_PATH"",
    ""0.3 AI-Regelwerk & Historie/Systemregeln/memory/json_memory_index.json""
)

# Globaler Kontext – Laufzeit-Gedächtnis
GPT_CONTEXT = {}

def update_context(new_data: dict) -> None:
    """"""
    Aktualisiert den globalen GPT-Kontext zur Laufzeit.
    """"""
    GPT_CONTEXT.update(new_data)

def get_context_value(key: str, default=None):
    """"""
    Gibt einen bestimmten Wert aus dem aktuellen GPT-Kontext zurück.
    """"""
    return GPT_CONTEXT.get(key, default)

def refresh_context() -> dict:
    """"""
    Lädt alle System- und Memory-Daten neu – ideal bei dynamischer Systemveränderung.
    """"""
    system_identity = checked_load_json(SYSTEM_IDENTITY_PATH, ""SYSTEM_IDENTITY_PATH"")
    index_data = checked_load_json(INDEX_PATH, ""INDEX_PATH"")
    memory_index = checked_load_json(MEMORY_INDEX_PATH, ""MEMORY_INDEX_PATH"")

    session_context = get_context_sessions()
    conversation_context = get_conversation_context()
    memory_log = get_memory_log()

    new_context = {
        ""system_identity"": system_identity,
        ""index"": index_data,
        ""memory_index"": memory_index,
        ""session_context"": session_context,
        ""conversation_context"": conversation_context,
        ""memory_log"": memory_log
    }

    update_context(new_context)
    print(""[GPTAgent] Kontext wurde aktualisiert."")  # Optionales Logging
    return new_context
