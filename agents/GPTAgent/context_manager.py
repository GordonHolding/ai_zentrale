# context_manager.py
# Verwalter des GPT-Runtime-Kontexts – nutzt RAM-basierten Kontextspeicher

from utils.json_loader import load_json_from_gdrive
from agents.GPTAgent.context_memory import set_context, get_context, clear_context

# Optional: robuste Imports für MemoryAgent
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

# GPT-Konfiguration laden
config = load_json_from_gdrive("gpt_config.json")

# Konfigurationspfade aus gpt_config.json
SYSTEM_IDENTITY_PATH = config.get("SYSTEM_IDENTITY_PATH", "system_identity_prompt.json")
INDEX_PATH = config.get("INDEX_PATH", "index.json")


def refresh_context() -> dict:
    """Lädt alle kontextrelevanten Daten neu – System, Index, Memory, Registry – und speichert sie im RAM-Store."""
    system_identity = load_json_from_gdrive(SYSTEM_IDENTITY_PATH)
    index_data = load_json_from_gdrive(INDEX_PATH)
    json_index = load_json_from_gdrive("json_file_index.json")
    agent_registry = load_json_from_gdrive("agent_registry.json")
    system_modules = load_json_from_gdrive("system_modules.json")

    session_context = get_context_sessions()
    conversation_context = get_conversation_context()
    memory_log = get_memory_log()

    new_context = {
        "system_identity": system_identity,
        "index": index_data,
        "json_index": json_index,
        "agent_registry": agent_registry,
        "system_modules": system_modules,
        "session_context": session_context,
        "conversation_context": conversation_context,
        "memory_log": memory_log
    }

    # In den zentralen Kontextspeicher schreiben
    for key, value in new_context.items():
        set_context(key, value)

    print("[GPTAgent] Kontext wurde aktualisiert und gespeichert.")
    return new_context


def get_context_value(key: str, default=None):
    """Liest Kontextwert aus dem RAM-Store."""
    return get_context(key) or default


def update_context(new_data: dict) -> None:
    """Optional: gezielte Aktualisierung einzelner Kontexteinträge."""
    for key, value in new_data.items():
        set_context(key, value)
