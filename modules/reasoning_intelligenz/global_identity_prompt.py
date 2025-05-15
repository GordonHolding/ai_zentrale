# global_identity_prompt.py

from agents.Infrastructure_Agents.RouterAgent.router_prompt_loader import load_identity_prompt

def get_system_prompt():
    """
    Gibt den zentralen AI-Zentrale-Identitätsprompt als String zurück
    """
    return load_identity_prompt()
