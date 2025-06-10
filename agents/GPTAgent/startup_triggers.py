# agents.GPTAgent.startup_triggers.py

from agents.GPTAgent.gpt_agent import startup
from agents.GPTAgent.context_manager import get_context_value
from utils.json_loader import load_json

# Hilfsfunktion für robustes JSON-Laden mit Fehlerprüfung
def checked_load_json(filename, context_hint):
    data = load_json(filename)
    if not isinstance(data, dict) or ""error"" in data:
        raise RuntimeError(
            f""Fehler beim Laden von '{context_hint}': {data.get('error') if isinstance(data, dict) else 'Unbekannter Fehler'}""
        )
    return data

CONFIG = checked_load_json(""gpt_config.json"", ""GPT-Konfiguration"")
ENABLE_LOGGING = CONFIG.get(""ENABLE_LOGGING"", True)

# Wird bei Systemstart oder Sessionstart aufgerufen
def trigger_startup_sequence():
    context = startup()

    if ENABLE_LOGGING:
        session_id = get_context_value(""session_id"", default=""UNKNOWN"")
        print(f""[GPTAgent] Initialisiert mit Session: {session_id}"")

    return context
