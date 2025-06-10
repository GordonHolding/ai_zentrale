# agents.GPTAgent.startup_loader.py

from utils.json_loader import load_json
from agents.GPTAgent.context_manager import update_context

CONFIG = load_json(""gpt_config.json"")


# Hilfsfunktion für robustes JSON-Laden mit Fehlerprüfung
def checked_load_json(filename, context_hint):
    data = load_json(filename)
    if not isinstance(data, dict) or ""error"" in data:
        raise RuntimeError(
            f""Fehler beim Laden von '{context_hint}': {data.get('error') if isinstance(data, dict) else 'Unbekannter Fehler'}""
        )
    return data


def initialize_system_context():
    """"""
    Lädt alle Kerninformationen für den GPTAgent bei Systemstart.
    """"""
    try:
        system_identity = checked_load_json(
            CONFIG.get(""SYSTEM_IDENTITY_PATH"", ""system_identity_prompt.json""),
            ""Systemidentität""
        )
    except Exception as e:
        print(f""[GPTAgent] Fehler beim Laden der Systemidentität: {e}"")
        system_identity = {}

    try:
        index_data = checked_load_json(
            CONFIG.get(""INDEX_PATH"", ""index.json""),
            ""Indexdaten""
        )
    except Exception as e:
        print(f""[GPTAgent] Fehler beim Laden der Indexdaten: {e}"")
        index_data = {}

    try:
        memory_index = checked_load_json(
            CONFIG.get(""MEMORY_INDEX_PATH"", ""json_memory_index.json""),
            ""Memory-Index""
        )
    except Exception as e:
        print(f""[GPTAgent] Fehler beim Laden des Memory-Index: {e}"")
        memory_index = {}

    projects = {}
    for path in CONFIG.get(""PROJECT_STRUCTURE_PATHS"", []):
        try:
            projects[path] = checked_load_json(path, f""Projektstruktur ({path})"")
        except Exception as e:
            print(f""[GPTAgent] Projektstruktur konnte nicht geladen werden: {path} ({e})"")
            continue

    context = {
        ""system_identity"": system_identity,
        ""index"": index_data,
        ""memory_index"": memory_index,
        ""project_structures"": projects
    }

    update_context(context)
    print(""[GPTAgent] Systemkontext wurde initialisiert."")  # Optionales Logging für Transparenz
    return context
