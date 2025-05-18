# time_based_trigger_checker.py

import os
import json
import datetime
from modules.output_infrastruktur.mail_tools import send_reminder_mail  # optional
from modules.reasoning_intelligenz.reminder_engine import trigger_custom_action  # frei definierbar

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

            trigger_time = trigger.get("time")  # Format: "14:00"
            trigger_day = trigger.get("day")  # Optional: "Monday", "daily"

            now_str = current_time.strftime("%H:%M")
            weekday_str = current_time.strftime("%A")

            if (trigger_day.lower() == "daily" or trigger_day == weekday_str) and now_str == trigger_time:
                # Triggeraktion ausführen
                trigger_custom_action(trigger)  # oder eigene Engine
                executed.append(trigger["name"])

        except Exception as e:
            executed.append(f"{trigger.get('name', 'Unbekannt')} ❌ Fehler: {e}")

    return executed
