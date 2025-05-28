# gpt_response_parser.py – GPT-Analyse mit Rolle, Trigger, Memorylogik

from utils.json_loader import load_json
from utils.context_manager import get_context
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# 🧠 Holt den aktiven Systemkontext aus dem context_manager
def get_system_context():
    return {
        "identity": get_context("identity"),
        "index": get_context("index"),
        "structure": get_context("projects")  # ersetzt get_all_structures()
    }

# 🎭 Rolle erkennen, z. B. „MarketingAgent“ oder „MailAgent“
def extract_role(response: str, identity_data: dict) -> str:
    roles = identity_data.get("rollen", {})
    for key, role in roles.items():
        if key.lower() in response.lower():
            return key
    return "unbekannt"

# 🎯 Systemtrigger erkennen (z. B. Speicher-, Export- oder Routing-Befehle)
def detect_system_trigger(response: str) -> str:
    triggers = ["save", "export", "memory", "route", "tool"]
    for keyword in triggers:
        if keyword in response.lower():
            return keyword
    return ""

# 📝 Antwortanalyse im Memory loggen
def log_response_analysis(user_input: str, gpt_reply: str):
    log_interaction(
        user="Parser",
        prompt=user_input,
        response=gpt_reply,
        path="memory_log.json"
    )

# 🧩 Hauptfunktion zur GPT-Antwortanalyse
def parse_gpt_response(user_input: str, gpt_reply: str) -> dict:
    context = get_system_context()
    role = extract_role(gpt_reply, context["identity"])
    action = detect_system_trigger(gpt_reply)

    return {
        "role": role,
        "trigger": action,
        "summary": gpt_reply[:200],
        "identity_prompt_used": context["identity"].get("system_name", "Unbekannt"),
        "project_count": len(context["structure"]),
        "user_input": user_input,
   
