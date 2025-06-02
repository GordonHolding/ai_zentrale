# trigger_router.py – Leitet Trigger an die passende Routine weiter (GPT-kompatibel)

from agents.Infrastructure_Agents.TriggerAgent.trigger_runner import run_routine
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_routing_error

# 🔀 Routet eine Liste erkannter Trigger zu den passenden Routinen
def route_triggers(trigger_list: list) -> list:
    results = []

    for trigger in trigger_list:
        try:
            if trigger["type"] == "gpt_trigger":
                result = run_routine(trigger["name"], source="GPT")
            elif trigger["type"] == "time_trigger":
                result = run_routine(trigger["name"], source="Time")
            elif trigger["type"] == "watcher_trigger":
                result = run_routine(trigger["name"], source="Watcher")
            elif trigger["type"] == "manual_trigger":
                result = run_routine(trigger["name"], source="Manual")
            else:
                result = f"⚠️ Unbekannter Trigger-Typ: {trigger.get('type')}"
            results.append(result)
        except Exception as e:
            log_routing_error(trigger, str(e))
            results.append(f"❌ Fehler bei Routing für Trigger: {trigger.get('name')}")

    return results

# ▶ Testfunktion
if __name__ == "__main__":
    test = [{"type": "gpt_trigger", "name": "trigger_cleanup_now"}]
    out = route_triggers(test)
    for res in out:
        print(res)
