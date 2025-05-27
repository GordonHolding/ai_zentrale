# agent_loader.py – Lädt alle Agenten aus agent_registry.json über json_loader

import importlib
from utils.json_loader import load_json

# ✅ Lade die Registry dynamisch (ohne harten Pfad)
AGENT_REGISTRY = load_json("agent_registry.json")

def get_all_agents():
    """Gibt die vollständige Agenten-Registry zurück"""
    return AGENT_REGISTRY

def get_active_agents():
    """Gibt nur die aktiven Agenten (active: true) zurück"""
    return [agent for agent in AGENT_REGISTRY if agent.get("active", False)]

def load_agent_by_filename(filename: str):
    """Lädt einen Agenten anhand des Dateinamens"""
    for agent in AGENT_REGISTRY:
        if agent.get("filename") == filename and agent.get("active", False):
            module_path = agent["import_path"]
            return import_agent(module_path)
    return None

def load_agent_by_import_path(import_path: str):
    """Lädt einen Agenten anhand des Importpfads"""
    for agent in AGENT_REGISTRY:
        if agent.get("import_path") == import_path and agent.get("active", False):
            return import_agent(import_path)
    return None

def import_agent(import_path: str):
    """Importiert und gibt das Agentenmodul zurück"""
    try:
        module = importlib.import_module(import_path)
        return module
    except Exception as e:
        print(f"❌ Fehler beim Laden von {import_path}: {e}")
        return None
