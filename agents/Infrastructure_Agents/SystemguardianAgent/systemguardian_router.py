# systemguardian_router.py

from .systemguardian_agent import analyze_logs_and_notify
from .systemguardian_triggers import escalate_security_incident

def handle_guardian_input(user_input: str):
    """
    Führt eine Guardian-Aktion basierend auf Textinput aus.
    """
    user_input = user_input.lower()

    if "systemstatus" in user_input or "bericht" in user_input:
        return analyze_logs_and_notify()

    if "sicherheitsmeldung" in user_input:
        message = "Möglicher unautorisierter Zugriff auf sensiblen Speicherbereich erkannt."
        escalate_security_incident(message)
        return "⚠️ Sicherheitsmeldung ausgelöst."

    return "🛡️ Kein Guardian-Befehl erkannt."
