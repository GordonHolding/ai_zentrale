# agents/Infrastructure_Agents/TriggerAgent/trigger_agent.py

from datetime import datetime
import traceback

from utils.json_loader import load_json, write_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import (
    log_trigger_execution,
    log_trigger_error,
    update_trigger_state
)
from agents.Infrastructure_Agents.TriggerAgent.trigger_triggers import run_all_triggers

TRIGGER_NAME = "TriggerAgent"

def execute_trigger_cycle():
    try:
        # 🔄 Konfiguration laden (aus Google Drive, GPT-kompatibel)
        config = load_json("trigger_config.json")
        if "error" in config:
            raise ValueError(f"⚠️ Trigger-Konfiguration nicht gefunden: {config['error']}")

        # 📎 Prompt-Definitionen laden (für spätere GPT-Integration)
        prompts = load_json("trigger_prompts.json")
        if "error" in prompts:
            prompts = {}
        else:
            print(f"📎 Trigger-Prompts geladen: {len(prompts)} Einträge")

        timestamp = datetime.utcnow().isoformat()

        # ▶ Triggers ausführen
        triggered_items = run_all_triggers(config)

        # 💾 Trigger-Zustand speichern
        update_trigger_state("trigger_state.json", triggered_items, timestamp)

        # 🪵 Erfolg loggen
        log_trigger_execution(trigger_name=TRIGGER_NAME, items=triggered_items, timestamp=timestamp)

        return {
            "status": "ok",
            "triggered": triggered_items,
            "timestamp": timestamp
        }

    except Exception as e:
        tb = traceback.format_exc()
        log_trigger_error(trigger_name=TRIGGER_NAME, error=str(e), traceback_str=tb)
        return {
            "status": "error",
            "error": str(e),
            "traceback": tb
        }

# ▶ Manuell startbar (z. B. bei Startup-Trigger)
if __name__ == "__main__":
    result = execute_trigger_cycle()
    print(result)
