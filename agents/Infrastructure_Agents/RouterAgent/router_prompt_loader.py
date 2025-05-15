import json
import os

IDENTITY_PROMPT_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.3 AI-Regelwerk & Historie/Systemregeln/system_identity_prompt.json"
AGENT_REGISTRY_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/Infrastructure_Agents/RouterAgent/Router_Memory/agent_registry.json"

def load_identity_prompt():
    try:
        with open(IDENTITY_PROMPT_PATH) as f:
            return json.load(f)["prompt"]
    except Exception as e:
        return f"Fehler beim Laden des Systemprompts: {e}"

def load_dynamic_router_prompt():
    try:
        with open(AGENT_REGISTRY_PATH) as f:
            agents = json.load(f)
        agent_list = "\n".join([f"• {v['name']} – {v['description']}" for v in agents.values()])
        return f"🧠 Die folgenden Agenten stehen dir zur Verfügung:\n{agent_list}"
    except Exception as e:
        return f"Fehler beim Laden der Agentenliste: {e}"
