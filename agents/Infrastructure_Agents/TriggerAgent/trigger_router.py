# trigger_router.py – Leitet Trigger an die passende Routine weiter (GPT-kompatibel)

from agents.Infrastructure_Agents.TriggerAgent.trigger_runner import run_routine
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_routing_error

# 🔀 Routet eine Liste erkannter Trigger zu den passenden Routinen
def route_triggers(trigger_list: list) -> list:
    results = []

    for trigger in trigger_list:
        try:
            trigger_name = trigger.get("name", "Unbekannt")
            trigger_type = trigger.get("type", "undefined")
            trigger_source = trigger.get("source", "unspecified")

            result = run_routine(trigger_name)
            results.append(f"▶ {trigger_type.upper()} → {trigger_name} → {result}")
        except Exception as e:
            log_routing_error(trigger, str(e))
            results.append(f"❌ Fehler bei Routing für Trigger: {trigger.get('name', 'Unbekannt')}")
    
    return results

# ▶ Testfunktion
if __name__ == "__main__":
    test = [{"type": "gpt_trigger", "name": "run_time_trigger", "source": "GPT"}]
    out = route_triggers(test)
    for res in out:
        print(res)
