# agents.GPTAgent.context_manager.py

from utils.json_loader import load_json_from_gdrive

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

# Globaler Kontext (GPT-Runtime)
GPT_CONTEXT = {}

def update_context(new_data: dict) -> None:
    """Aktualisiert den globalen GPT-Kontext zur Laufzeit."""
    GPT_CONTEXT.update(new_data)

def get_context_value(key: str, default=None):
    """Gibt einen bestimmten Wert aus dem aktuellen GPT-Kontext zurück."""
    return GPT_CONTEXT.get(key, default)

def refresh_context() -> dict:
    """Lädt alle kontextrelevanten Daten neu – System, Index, Memory, Registry."""
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

    update_context(new_context)
    print("[GPTAgent] Kontext wurde aktualisiert.")
    return new_context
