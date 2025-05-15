# interface_agent.py

from interface_router import determine_agent
from interface_config import AGENT_LABELS, DEFAULT_MAIL_ACCOUNT
from interface_triggers import post_action_trigger

from mail_agent import process_emails
from memory_agent import search_memory

def handle_user_input(user_input):
    """
    Zentrale Steuerlogik für den InterfaceAgent.
    """

    agent_key = determine_agent(user_input)

    if agent_key == "mail":
        print("📬 MailAgent wird aktiviert...")
        result = process_emails(DEFAULT_MAIL_ACCOUNT)
        post_action_trigger("mail", result)

    elif agent_key == "memory":
        print("🧠 MemoryAgent wird aktiviert...")
        result = search_memory("florian")  # später dynamisch per GPT
        post_action_trigger("memory", result)

    else:
        print("🤷‍♂️ Ich konnte keinen zuständigen Agenten erkennen.")
        return "Keine Aktion ausgeführt."

if __name__ == "__main__":
    user_input = input("Was möchtest du tun? ").strip()
    handle_user_input(user_input)
