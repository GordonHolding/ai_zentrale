# agents.GPTAgent.startup_loader.py

from utils.json_loader import load_json
from agents.GPTAgent.context_manager import update_context

CONFIG = load_json("gpt_config.json")

def initialize_system_context():
    """
    Lädt alle Kerninformationen für den GPTAgent bei Systemstart.
    """
    system_identity = load_json(CONFIG.get("SYSTEM_IDENTITY_PATH", "system_identity_prompt.json"))
    index_data = load_json(CONFIG.get("INDEX_PATH", "index.json"))
    memory_index = load_json(CONFIG.get("MEMORY_INDEX_PATH", "json_memory_index.json"))
    
    projects = {}
    for path in CONFIG.get("PROJECT_STRUCTURE_PATHS", []):
        try:
            projects[path] = load_json(path)
        except Exception:
            continue

    context = {
        "system_identity": system_identity,
        "index": index_data,
        "memory_index": memory_index,
        "project_structures": projects
    }

    update_context(context)
    return context
