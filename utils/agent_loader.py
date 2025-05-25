# utils/agent_loader.py – Dynamische Agentenerkennung via GPT-Logik & Google Drive

import importlib
from utils.json_loader import get_json_by_keyword

def load_agent_registry():
    """
    Lädt das Agenten-Registry aus dem zentralen Google-Drive-Systemverzeichnis
    via Keyword-Erkennung (z. B. agent_registry.json)
    """
    registry = get_json_by_keyword("agent_registry")
    if "error" in registry:
        raise ValueError(f"Fehler beim Laden der Agenten-Registry: {registry['error']}")
    return registry

def execute_agent(agent_key, user_input):
    """
    Führt die definierte Funktion eines registrierten Agenten aus.
    """
    registry = load_agent_registry()

    if agent_key not in registry:
        return f"❌ Agent '{agent_key}' nicht registriert."

    agent_info = registry[agent_key]

    try:
        module = importlib.import_module(agent_info["module"])
        func = getattr(module, agent_info["function"])
        args = [user_input if a == "user_input" else os.getenv(a, a) for a in agent_info.get("args", [])]
        return func(*args)
    except Exception as e:
        return f"❌ Fehler beim Ausführen von Agent '{agent_key}': {e}"
