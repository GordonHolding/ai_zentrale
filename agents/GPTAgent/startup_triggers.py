# agents.GPTAgent.startup_triggers.py

from agents.GPTAgent.gpt_agent import startup
from agents.GPTAgent.context_manager import get_context_value
from agents.GPTAgent.context_memory import get_context_value as get_context_from_memory

# Wird bei Systemstart oder Sessionstart aufgerufen
def trigger_startup_sequence():
    context = startup()

    # Logging prüfen aus RAM-Konfiguration
    config = get_context_from_memory("gpt_config") or {}
    enable_logging = config.get("LOGGING", {}).get("value", True)

    if enable_logging:
        session_id = get_context_value("session_id") or "UNKNOWN"
        print(f"[GPTAgent] Initialisiert mit Session: {session_id}")

    return context
