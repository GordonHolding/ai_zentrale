# startup_loader.py – Direkter Systemstart mit Klartextstruktur

from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

def get_identity_prompt():
    return load_json("system_identity_prompt.json")

def get_index():
    return load_json("index.json")

def get_all_structures():
    index = get_index()
    structure_files = {}
    for entry in index.get("structure_files", []):
        file = entry.get("filename")
        key = entry.get("key") or file.replace(".json", "")
        structure_files[key] = load_json(file)
    return structure_files

def load_prompt_for_project(project_key="global"):
    if project_key == "global":
        return get_identity_prompt()
    # Falls später Projektprompts ergänzt werden
    return {}

def log_system_start():
    prompt = get_identity_prompt()
    log_interaction(
        user="System",
        prompt="Systemstart – Lade identity_prompt",
        response=f"Aktive Rollen: {', '.join(prompt.get('rollen', {}).keys())}",
        path="memory_log.json"
    )
