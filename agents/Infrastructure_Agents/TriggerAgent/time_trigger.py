# time_trigger.py – vereinte Zeitlogik für geplante Trigger, Deadlines & Erinnerungen

from datetime import datetime, timedelta
from utils.json_loader import load_json
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from agents.General_Agents.CalendarAgent.calendar_reader import get_all_deadlines
from agents.Infrastructure_Agents.TriggerAgent.trigger_custom_action import execute_trigger_action

# 🔁 Zeitbasierte Trigger ausführen (z. B. 09:00 täglich)
def run_scheduled_triggers(current_time=None):
    config = load_json("trigger_config.json")
    if not config or "scheduled_triggers" not in config:
        return ["⚠️ Keine geplanten Trigger gefunden."]

    current_time = current_time or datetime.now()
    now_str = current_time.strftime("%H:%M")
    weekday_str = current_time.strftime("%A")

    results = []
    for trig in config["scheduled_triggers"]:
        try:
            if not trig.get("enabled", True):
                continue
            trig_time = trig.get("time", "")
            trig_day = trig.get("day", "").lower()

            if (trig_day == "daily" or trig_day == weekday_str.lower()) and now_str == trig_time:
                result = execute_trigger_action(trig)
                results.append(f"✅ {trig['name']} ausgeführt → {result}")
        except Exception as e:
            results.append(f"❌ Fehler bei Trigger '{trig.get('name', 'Unbenannt')}': {e}")
    return results

# ⏰ Deadline-Überprüfung (fällig oder überfällig)
def check_deadline_warnings():
    today = datetime.today().date()
    upcoming_days = 3
    warnings = []

    for deadline in get_all_deadlines():
        try:
            due = datetime.strptime(deadline["due_date"], "%Y-%m-%d").date()
            delta = (due - today).days
            if delta < 0:
                warnings.append(f"⏰ Überfällig: {deadline['key']} (seit {abs(delta)} Tagen) – {deadline['source']}")
            elif 0 <= delta <= upcoming_days:
                warnings.append(f"⚠️ Bald fällig: {deadline['key']} (in {delta} Tagen) – {deadline['source']}")
        except Exception:
            continue
    return warnings

# 🔔 Erinnerungslogik auf Basis von Deadlines
def run_reminder_from_deadlines():
    warnings = check_deadline_warnings()
    if not warnings:
        return "✅ Keine kritischen Fristen erkannt."

    log_interaction("System", {
        "type": "Reminder",
        "entries": warnings,
        "timestamp": datetime.now().isoformat()
    })

    return "🔔 Erinnerung aktiv:\n" + "\n".join(warnings)

# 🧠 Hauptfunktion zur kombinierten Ausführung aller Zeittrigger
def run_time_trigger_routine():
    logs = []

    # ⏱️ Zeitbasierte Trigger
    logs += run_scheduled_triggers()

    # ⏰ Fristen prüfen + Erinnerungen generieren
    reminder_result = run_reminder_from_deadlines()
    logs.append(reminder_result)

    return logs

# ▶️ Direkte Ausführung (optional via CLI)
if __name__ == "__main__":
    results = run_time_trigger_routine()
    for r in results:
        print(f"[TRIGGER] {r}")
