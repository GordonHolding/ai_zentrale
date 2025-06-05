# router_agent.py

import importlib
from agents.Infrastructure_Agents.RouterAgent.router_router import determine_agent
from agents.Infrastructure_Agents.TriggerAgent.trigger_router import post_action_trigger
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from utils.json_loader import load_json

def execute_agent(agent_key, user_input):
    """
    Lädt den gewünschten Agent aus agent_registry.json dynamisch und führt ihn aus.
    """
    try:
        agents = load_json("agent_registry.json")
        agent = agents.get(agent_key)
    except Exception as e:
        return f"❌ Fehler beim Laden der Agentenliste: {e}"

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
    """
    Routet den User Input über GPT, ruft den Ziel-Agenten auf und loggt das Ergebnis.
    """
    try:
        agent_key = determine_agent(user_input)
        if agent_key and isinstance(agent_key, str) and agent_key != "none":
            log_interaction("RouterAgent", f"🔁 Routing an: {agent_key}", user_input)
            result = execute_agent(agent_key, user_input)
            post_action_trigger(agent_key, result)
            return result
        else:
            log_interaction("RouterAgent", "❓ Kein zuständiger Agent erkannt", user_input)
            return "Keine Aktion ausgeführt."
    except Exception as e:
        return f"❌ Fehler im RouterAgent: {e}"

if __name__ == "__main__":
    print("🧠 RouterAgent ist aktiv.")
    user_input = input("Was möchtest du tun? ").strip()
    output = handle_user_input(user_input)
    print(output)
