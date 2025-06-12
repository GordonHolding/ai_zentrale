# agents.GPTAgent.startup_loader.py

from utils.json_loader import load_json_from_gdrive
from agents.GPTAgent.context_manager import update_context


def initialize_system_context():
    """
    Lädt alle Kerninformationen für den GPTAgent bei Systemstart – 
    inkl. Systemprompt, Indexdaten, Strukturdateien und json_file_index.
    """

    # GPT-Agent-Konfiguration laden
    config = load_json_from_gdrive("gpt_config.json")

    # Kerninformationen laden
    system_identity = load_json_from_gdrive(config.get("SYSTEM_IDENTITY_PATH", "system_identity_prompt.json"))
    index_data = load_json_from_gdrive(config.get("INDEX_PATH", "index.json"))
    json_index = load_json_from_gdrive("json_file_index.json")

    # Strukturdateien aus config laden (PROJECT_STRUCTURE_PATHS)
    project_structures = {}
    for path in config.get("PROJECT_STRUCTURE_PATHS", []):
        try:
            project_structures[path] = load_json_from_gdrive(path)
        except Exception as e:
            print(f"[GPTAgent] Strukturdatei konnte nicht geladen werden: {path} ({e})")
            continue

    # Gesamtkontext bauen
    context = {
        "system_identity": system_identity,
        "index": index_data,
        "json_index": json_index,
        "project_structures": project_structures
    }

    # Kontext übergeben
    update_context(context)
    print("[GPTAgent] Systemkontext wurde initialisiert.")

    return context
