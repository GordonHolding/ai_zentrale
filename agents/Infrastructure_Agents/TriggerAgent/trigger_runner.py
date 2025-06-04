# agents/Infrastructure_Agents/TriggerAgent/trigger_runner.py

from datetime import datetime
from agents.Infrastructure_Agents.TriggerAgent.time_trigger import run_time_trigger_routine
from agents.Infrastructure_Agents.TriggerAgent.custom_action import execute_trigger_action
from agents.Infrastructure_Agents.TriggerAgent.watcher_trigger import run_drive_watcher_scan
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_trigger_execution

# ▶ Hauptfunktion: Führe eine Routine basierend auf Trigger-Namen aus
def run_routine(trigger_name: str, source: str = "System") -> str:
    timestamp = datetime.utcnow().isoformat()
    log_trigger_execution("TriggerRunner", [trigger_name], timestamp)

    try:
        # 💡 Zeitbasierte Routinen
        if trigger_name in ("run_time_trigger", "check_scheduled_tasks", "morning_trigger"):
            return "\n".join(run_time_trigger_routine())

        # 💡 Dateiüberwachung
        elif trigger_name in ("scan_drive_structure", "watch_for_new_files"):
            return run_drive_watcher_scan()

        # 💡 Benutzerdefinierte Aktion aus JSON-TriggerConfig
        else:
            result = execute_trigger_action({"name": trigger_name})
            return f"✅ Trigger '{trigger_name}' ({source}) ausgeführt → {result}"

    except Exception as e:
        return f"❌ Fehler bei Trigger '{trigger_name}' ({source}): {e}"

# ▶ Direktes Testing
if __name__ == "__main__":
    test = run_routine("run_time_trigger", source="Manual Test")
    print(test)
