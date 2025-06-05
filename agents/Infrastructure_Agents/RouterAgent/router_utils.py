# router_utils.py

from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

def get_structure_snippet():
    try:
        structure_data = load_json("00_ai_zentrale_masterstruktur.json")

        core_info = {
            "Zentrale Steuerung": structure_data.get("Zentrale Steuerung", "Nicht definiert"),
            "Agentenarchitektur": structure_data.get("Agentenarchitektur", "Nicht definiert"),
            "Ebenen": structure_data.get("Ebenen", "Nicht definiert"),
            "Navigationslogik": structure_data.get("Navigationslogik", "Nicht definiert")
        }

        snippet = "\n".join([f"🔹 {k}: {v}" for k, v in core_info.items()])
        return snippet
    except Exception as e:
        log_interaction("RouterUtils", f"❌ Fehler beim Laden des Struktur-Snippets: {e}", "")
        return "Strukturauszug konnte nicht geladen werden."
