# agents.GPTAgent.gpt_response_parser.py

from utils.json_loader import load_json
from agents.GPTAgent.context_manager import get_context_value
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# GPT-Konfiguration laden
CONFIG = load_json(""gpt_config.json"")
PROMPT_PATH = CONFIG.get(""PROMPT_PATH"", ""gpt_agent_prompt.json"")

# Systemkontext abrufen
def get_system_context():
    return {
        ""identity"": get_context_value(""system_identity""),
        ""index"": get_context_value(""index""),
        ""memory_index"": get_context_value(""memory_index""),
        ""session"": get_context_value(""session_context""),
        ""conversation"": get_context_value(""conversation_context""),
        ""memory_log"": get_context_value(""memory_log"")
    }

# 🎭 Rolle erkennen – basierend auf Rollen aus system_identity_prompt.json
def extract_role(response: str, identity_data: dict) -> str:
    roles = identity_data.get(""rollen"", {})
    for key, role in roles.items():
        if key.lower() in response.lower():
            return key
    return ""unbekannt""

# 🎯 Systemtrigger erkennen – z. B. „save“, „route“, „tool“, „export“
def detect_system_trigger(response: str) -> str:
    triggers = [""save"", ""export"", ""memory"", ""route"", ""tool"", ""trigger""]
    for keyword in triggers:
        if keyword in response.lower():
            return keyword
    return """"

# 📝 GPT-Antwort im Memory loggen (als „Verständnisanalyse“)
def log_response_analysis(user_input: str, gpt_reply: str):
    log_interaction(
        user=""GPTParser"",
        prompt=user_input,
        response=gpt_reply,
        path=""memory_log.json""
    )

# 🧩 Hauptfunktion zur Analyse einer GPT-Antwort
def parse_gpt_response(user_input: str, gpt_reply: str) -> dict:
    context = get_system_context()
    role = extract_role(gpt_reply, context[""identity""])
    trigger = detect_system_trigger(gpt_reply)

    # Logging
    log_response_analysis(user_input, gpt_reply)

    return {
        ""role"": role,
        ""trigger"": trigger,
        ""summary"": gpt_reply[:200],
        ""user_input"": user_input,
        ""raw_response"": gpt_reply,
        ""context_project_count"": len(context.get(""index"", {})),
        ""used_prompt"": PROMPT_PATH,
        ""memory_context_available"": bool(context.get(""memory_log""))
    }
