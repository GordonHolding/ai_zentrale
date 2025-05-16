# utils/agent_loader.py
import importlib
import json
import os

REGISTRY_PATH = "config/agent_registry.json"

def load_agent_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def execute_agent(agent_key, user_input):
    registry = load_agent_registry()
    if agent_key not in registry:
        return f"❌ Agent {agent_key} nicht registriert."

    agent_info = registry[agent_key]
    module = importlib.import_module(agent_info["module"])
    func = getattr(module, agent_info["function"])
    args = [user_input if a == "user_input" else os.getenv(a, a) for a in agent_info["args"]]
    return func(*args)
