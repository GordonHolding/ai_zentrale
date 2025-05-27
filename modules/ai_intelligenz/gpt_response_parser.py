# gpt_response_parser.py – GPT-Analyse mit Rolle, Trigger, Memorylogik

from utils.json_loader import load_json
from modules.reasoning_intelligenz.structure_content_loader import get_all_structures
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

def get_system_context():
    return {
        "identity": load_json("system_identity_prompt.json"),
        "index": load_json("index.json"),
        "structure": get_all_structures()
    }

def extract_role(response: str, identity_data: dict) -> str:
    roles = identity_data.get("rollen", {})
    for key, role in roles.items():
        if key.lower() in response.lower():
            return key
    return "unbekannt"

def detect_system_trigger(response: str) -> str:
    triggers = ["save", "export", "memory", "route", "tool"]
    for keyword in triggers:
        if keyword in response.lower():
            return keyword
    return ""

def log_response_analysis(user_input: str, gpt_reply: str):
    log_interaction(
        user="Parser",
        prompt=user_input,
        response=gpt_reply,
        path="memory_log.json"
    )

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
        "raw_response": gpt_reply
    }
