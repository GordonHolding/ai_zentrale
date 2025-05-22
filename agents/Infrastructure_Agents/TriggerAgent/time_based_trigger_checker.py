# time_based_trigger_checker.py

import os
import json
import datetime
from modules.reasoning_intelligenz.trigger_custom_action import execute_trigger_action

CONFIG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/trigger_config.json"

def load_triggers():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def check_and_execute_triggers(current_time=None):
    if current_time is None:
        current_time = datetime.datetime.now()

    active_triggers = load_triggers()
    executed = []

    for trigger in active_triggers:
        try:
            if not trigger.get("enabled", True):
                continue

            trigger_time = trigger.get("time")  # z. B. "09:00"
            trigger_day = trigger.get("day")    # z. B. "Monday" oder "daily"

            now_str = current_time.strftime("%H:%M")
            weekday_str = current_time.strftime("%A")

            if (trigger_day.lower() == "daily" or trigger_day == weekday_str) and now_str == trigger_time:
                result = execute_trigger_action(trigger)
                executed.append(f"{trigger['name']} → {result}")

        except Exception as e:
            executed.append(f"{trigger.get('name', 'Unbekannt')} ❌ Fehler: {e}")

    return executed
