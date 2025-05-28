# startup_loader.py – Direkter Systemstart mit Kontextlogik

from infrastructure.context_manager import get_context, preload_all
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# 🔐 Identity Prompt laden
def get_identity_prompt():
    return get_context("identity")

# 🔐 Zentrales index.json laden
def get_index():
    return get_context("index")

# 📌 Optionales Laden von Projektprompts (künftige Nutzung)
def load_prompt_for_project(project_key="global"):
    if project_key == "global":
        return get_identity_prompt()
    return {}  # Erweiterbar für spezifische Projektkontexte

# 🧠 Systemstart loggen
def log_system_start():
    prompt = get_identity_prompt()
    aktive_rollen = prompt.get("rollen", {}).keys()
    log_interaction(
        user="System",
        prompt="Systemstart – Lade identity_prompt",
        response=f"Aktive Rollen: {', '.join(aktive_rollen)}",
        path="memory_log.json"
    )

# 🚀 Vollständiger Start: lädt alle Kontexte + loggt Systemstart
def full_system_start():
    preload_all()
    log_system_start()
