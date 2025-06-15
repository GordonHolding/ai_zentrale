# context_manager.py – GPT-RAM-Zugriffsmodul für alle Kontexte & JSONs

from agents.GPTAgent.context_memory import (
    get_context,
    update_context,
    get_context_value,
    get_json,
    get_prompt,
    get_config
)

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


def refresh_context() -> dict:
    """
    Aktualisiert den globalen GPT-Kontext zur Laufzeit durch erneutes Einlesen der relevanten JSONs aus RAM.
    (Alle Daten werden aus context_memory.py gezogen – kein GDrive-Zugriff)
    """

    new_context = {
        "system_identity": get_json("system_identity_prompt.json"),
        "index": get_json("index.json"),
        "json_index": get_json("json_file_index.json"),
        "agent_registry": get_json("agent_registry.json"),
        "system_modules": get_json("system_modules.json"),
        "session_context": get_context_sessions(),
        "conversation_context": get_conversation_context(),
        "memory_log": get_memory_log()
    }

    update_context(new_context)
    print("[GPTAgent] 🔄 Kontext wurde erfolgreich aktualisiert.")
    return new_context


# Shortcut: Einzelwert aus GPT-Kontext lesen
def get_context_value_safe(key: str, default=None):
    return get_context().get(key, default)
