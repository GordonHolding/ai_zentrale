# startup_loader.py – Initialisiert AI-Zentrale zum Startzeitpunkt

import json
from modules.reasoning_intelligenz.gpt_prompt_selector import load_prompt_for_project
from modules.reasoning_intelligenz.global_identity_prompt import get_system_prompt
from modules.reasoning_intelligenz.structure_content_loader import get_all_structures
from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_system_start

# Konfigurationspfade (im Drive abgelegt)
CONFIG_PATH = "0.4 GPT-Tools/startup_loader/startup_loader_config.json"
LOG_PATH = "0.4 GPT-Tools/startup_loader/startup_loader_log.json"
PROMPT_PATH = "0.4 GPT-Tools/startup_loader/startup_loader_prompt.json"
DRIVE_CONFIG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/drive_index_config.json"

def run_startup_initialization():
    """Führt alle Initial-Ladevorgänge beim Start der AI-Zentrale aus"""

    config = load_json(CONFIG_PATH)
    log_entries = []

    # 1. Lade System-Identitätsprompt
    identity_prompt = get_system_prompt()
    log_entries.append({"task": "identity_prompt_loaded", "content": identity_prompt})

    # 2. Lade Projekt-Prompt via gpt_prompt_selector
    project_prompt = load_prompt_for_project()
    log_entries.append({"task": "project_prompt_loaded", "content": project_prompt})

    # 3. Lade alle Strukturdefinitionen (für Navigation & GPT-Verständnis)
    structures = get_all_structures()
    log_entries.append({
        "task": "structure_files_loaded",
        "count": len(structures),
        "loaded_files": list(structures.keys())
    })

    # 4. Lade optionale Start-Prompts oder Hinweise (z. B. GPT-Moduswechsel)
    startup_prompt = load_json(PROMPT_PATH).get("startup_message", "")
    log_entries.append({"task": "startup_prompt", "content": startup_prompt})

    # 5. Prüfe Drive-Konfiguration (nur Logzweck)
    drive_config = load_json(DRIVE_CONFIG_PATH)
    if "root_folder_id" in drive_config:
        log_entries.append({"task": "drive_config_checked", "folder_id": drive_config["root_folder_id"]})
    else:
        log_entries.append({"task": "drive_config_missing_or_invalid"})

    # 6. Logge Systemstart
    log_system_start(LOG_PATH, log_entries)

    return {
        "status": "initialized",
        "identity": identity_prompt,
        "project_prompt": project_prompt,
        "startup_message": startup_prompt,
        "structures": list(structures.keys()),
        "drive_config": drive_config
    }
