# router_prompt_loader.py

from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

def get_system_identity_prompt():
    try:
        identity_data = load_json("system_identity_prompt.json")
        return identity_data.get("prompt", "Kein Systemprompt gefunden.")
    except Exception as e:
        log_interaction("RouterPromptLoader", f"❌ Fehler beim Laden des Identity-Prompts: {e}", "")
        return "Fehler beim Laden des Systemprompts."

def get_agent_registry_text():
    try:
        registry = load_json("agent_registry.json")
        agent_list = []
        for key, val in registry.items():
            if val.get("active", False):
                label = val.get("label", key)
                desc = val.get("description", "Kein Beschreibungstext")
                agent_list.append(f"– {key}: {label} – {desc}")
        return "\n".join(agent_list)
    except Exception as e:
        log_interaction("RouterPromptLoader", f"❌ Fehler beim Laden der Agentenliste: {e}", "")
        return "Fehler beim Laden der Agentenliste."
