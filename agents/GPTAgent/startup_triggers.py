# agents.GPTAgent.startup_triggers.py

from agents.GPTAgent.gpt_agent import startup
from agents.GPTAgent.context_manager import get_context_value
from utils.json_loader import load_json_from_gdrive

# GPT-Konfiguration laden
config = load_json_from_gdrive("gpt_config.json")
ENABLE_LOGGING = config.get("LOGGING", {}).get("value", True)

# Wird bei Systemstart oder Sessionstart aufgerufen
def trigger_startup_sequence():
    context = startup()

    if ENABLE_LOGGING:
        session_id = get_context_value("session_id") or "UNKNOWN"
        print(f"[GPTAgent] Initialisiert mit Session: {session_id}")

    return context
