# router_agent.py

from router_router import determine_agent
from router_config import AGENT_LABELS, DEFAULT_MAIL_ACCOUNT
from router_triggers import post_action_trigger

from mail_agent import process_emails
from memory_agent import search_memory

def handle_user_input(user_input):
    """
    Zentrale Steuerlogik für den RouterAgent.
    Erkennt Kontext, ruft richtigen Agent auf.
    """

    agent_key = determine_agent(user_input)

    if agent_key == "mail":
        print("📬 MailAgent wird aktiviert...")
        result = process_emails(DEFAULT_MAIL_ACCOUNT)
        post_action_trigger("mail", result)
        return result

    elif agent_key == "memory":
        print("🧠 MemoryAgent wird aktiviert...")
        # Dynamischer Suchbegriff aus dem Input könnte hier extrahiert werden
        result = search_memory(user_input)
        post_action_trigger("memory", result)
        return result

    else:
        print("❓ Kein zuständiger Agent erkannt.")
        return "Keine Aktion ausgeführt."

# Optional für lokalen CLI-Test
if __name__ == "__main__":
    user_input = input("Was möchtest du tun? ").strip()
    handle_user_input(user_input)
