# router_agent.py

from agents.Infrastructure_Agents.RouterAgent.router_router import determine_agent
from agents.Infrastructure_Agents.TriggerAgent.trigger_router import post_action_trigger
from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
import importlib

AGENT_REGISTRY_PATH = "agent_registry.json"  # oder via get_json_by_keyword("agents")

def execute_agent(agent_key, user_input):
    agents = load_json(AGENT_REGISTRY_PATH)
    agent = agents.get(agent_key)

    if not agent or not agent.get("active", False):
        return f"🚫 Agent '{agent_key}' ist nicht aktiv oder nicht registriert."

    try:
        module = importlib.import_module(agent["module"])
        func = getattr(module, agent["function"])
        args = [user_input] if "user_input" in agent.get("args", []) else []
        return func(*args)
    except Exception as e:
        return f"❌ Fehler beim Ausführen von Agent '{agent_key}': {e}"

def handle_user_input(user_input):
    agent_key = determine_agent(user_input)

    if agent_key and isinstance(agent_key, str):
        log_interaction("RouterAgent", f"🔁 Routing an: {agent_key}", user_input)
        result = execute_agent(agent_key, user_input)
        post_action_trigger(agent_key, result)
        return result
    else:
        log_interaction("RouterAgent", "❓ Kein zuständiger Agent erkannt", user_input)
        return "Keine Aktion ausgeführt."

if __name__ == "__main__":
    user_input = input("Was möchtest du tun? ").strip()
    output = handle_user_input(user_input)
    print(output)
