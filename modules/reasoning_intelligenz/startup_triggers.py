# startup_triggers.py – Triggerlogik bei Systemstart & Initialisierung

from modules.reasoning_intelligenz.startup_loader import (
    full_system_start,
    get_identity_prompt,
    load_prompt_for_project
)
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_system_start
from agents.Infrastructure_Agents.MemoryAgent.context_triggers import mark_session_start
import datetime

# 🚀 Startet das gesamte System inkl. Logging & Rollenabgleich
def trigger_full_system_start(user_id="System"):
    full_system_start()
    mark_session_start(user_id)
    return "✅ AI-Zentrale vollständig gestartet & neue Session initialisiert."

# 🔁 Nur Rollen aus Identity Prompt neu laden
def reload_identity_prompt():
    identity = get_identity_prompt()
    rollen = identity.get("rollen", {}).keys()
    return f"🔄 Identity Prompt geladen. Aktive Rollen: {', '.join(rollen)}"

# 📘 Manuelles Logging eines Starts (z. B. bei Teilstarts, Agent-Boot)
def log_manual_start_note():
    log_system_start()
    return f"📘 Systemstart manuell geloggt ({datetime.datetime.now().isoformat()})"

# 🧠 Optional: Projektspezifischer Prompt (nur bei Erweiterung sinnvoll)
def trigger_project_prompt_load(project_key):
    prompt = load_prompt_for_project(project_key)
    if not prompt:
        return f"⚠️ Kein Prompt für Projekt {project_key} gefunden."
    return f"📂 Prompt für Projekt {project_key} geladen."
