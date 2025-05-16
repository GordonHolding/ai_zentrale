# router_agent.py

from router_router import determine_agent
from router_triggers import post_action_trigger
from utils.agent_loader import execute_agent

def handle_user_input(user_input):
    """
    Dynamisches Agenten-Routing – erkennt Kontext und ruft passenden Agent auf.
    """
    agent_key = determine_agent(user_input)

    if agent_key:
        print(f"🧠 Agent erkannt: {agent_key} → wird ausgeführt.")
        result = execute_agent(agent_key, user_input)
        post_action_trigger(agent_key, result)
        return result
    else:
        print("❓ Kein zuständiger Agent erkannt.")
        return "Keine Aktion ausgeführt."

if __name__ == "__main__":
    user_input = input("Was möchtest du tun? ").strip()
    handle_user_input(user_input)
