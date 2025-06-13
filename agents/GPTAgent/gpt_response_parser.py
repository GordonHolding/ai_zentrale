# agents.GPTAgent.gpt_response_parser.py

from utils.json_loader import load_json_from_gdrive
from agents.GPTAgent.context_manager import get_context_value

# Optionaler Import: MemoryAgent-Logging
try:
    from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
except ImportError:
    def log_interaction(**kwargs):
        pass

# GPT-Konfiguration laden
config = load_json_from_gdrive("gpt_config.json")
PROMPT_PATH = config.get("PROMPT_PATH", "gpt_agent_prompt.json")


def get_system_context():
    """
    Gibt den aktuellen Systemkontext zurück – genutzt zur Reaktionseinordnung.
    """
    return {
        "identity": get_context_value("system_identity"),
        "index": get_context_value("index"),
        "json_index": get_context_value("json_index"),
        "agent_registry": get_context_value("agent_registry"),
        "system_modules": get_context_value("system_modules"),
        "session": get_context_value("session_context"),
        "conversation": get_context_value("conversation_context"),
        "memory_log": get_context_value("memory_log")
    }


def extract_role(response: str, identity_data: dict) -> str:
    """
    Erkennt die Rolle, auf die sich GPT bezieht – basierend auf system_identity_prompt.json.
    """
    roles = identity_data.get("rollen", {})
    for key, role in roles.items():
        if key.lower() in response.lower():
            return key
    return "unbekannt"


def detect_system_trigger(response: str) -> str:
    """
    Erkennt systemrelevante Trigger – z. B. 'save', 'route', 'export'.
    """
    triggers = ["save", "export", "memory", "route", "tool", "trigger"]
    for keyword in triggers:
        if keyword in response.lower():
            return keyword
    return ""


def log_response_analysis(user_input: str, gpt_reply: str):
    """
    Loggt eine GPT-Antwort zur Nachverfolgung in den memory_log.json.
    """
    log_interaction(
        user="GPTParser",
        prompt=user_input,
        response=gpt_reply,
        path="gpt_agent_memory_log.json"
    )


def parse_gpt_response(user_input: str, gpt_reply: str) -> dict:
    """
    Hauptfunktion: analysiert eine GPT-Antwort und extrahiert relevante Systemdaten.
    """
    context = get_system_context()
    role = extract_role(gpt_reply, context.get("identity", {}))
    trigger = detect_system_trigger(gpt_reply)

    # Analyseergebnis loggen
    log_response_analysis(user_input, gpt_reply)

    return {
        "role": role,
        "trigger": trigger,
        "summary": gpt_reply[:200],
        "user_input": user_input,
        "raw_response": gpt_reply,
        "context_project_count": len(context.get("index", {})),
        "used_prompt": PROMPT_PATH,
        "memory_context_available": bool(context.get("memory_log")),
        "agents_available": list(context.get("agent_registry", {}).keys()),
        "modules_loaded": list(context.get("system_modules", {}).keys())
    }
