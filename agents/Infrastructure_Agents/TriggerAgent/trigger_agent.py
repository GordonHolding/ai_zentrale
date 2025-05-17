# trigger_agent.py

import json
import importlib
import os
from datetime import datetime, timedelta

CONFIG_PATH = "config/trigger_config.json"
STATE_PATH = "agents/Infrastructure_Agents/TriggerAgent/TriggerAgent_Memory/trigger_state.json"
HISTORY_PATH = "agents/Infrastructure_Agents/TriggerAgent/TriggerAgent_Memory/trigger_history.json"
ERROR_PATH = "agents/Infrastructure_Agents/TriggerAgent/TriggerAgent_Protokolle/trigger_errors.json"
EXECUTION_LOG_PATH = "agents/Infrastructure_Agents/TriggerAgent/TriggerAgent_Protokolle/trigger_execution_log.json"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def execute_routine(name, routine):
    try:
        mod = importlib.import_module(routine["target_module"])
        func = getattr(mod, routine["target_function"])
        result = func()

        log = load_json(EXECUTION_LOG_PATH)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "routine": name,
            "result": str(result)[:200]
        }
        log.setdefault("runs", []).append(log_entry)
        save_json(EXECUTION_LOG_PATH, log)

        history = load_json(HISTORY_PATH)
        history[name] = log_entry["timestamp"]
        save_json(HISTORY_PATH, history)

    except Exception as e:
        errors = load_json(ERROR_PATH)
        errors.setdefault(name, []).append({
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        })
        save_json(ERROR_PATH, errors)

def check_triggers():
    config = load_json(CONFIG_PATH)
    last_run = load_json(HISTORY_PATH)

    for name, routine in config.items():
        if not routine.get("active"):
            continue

        last_exec = last_run.get(name)
        now = datetime.now()

        if not last_exec:
            execute_routine(name, routine)
            continue

        last_time = datetime.fromisoformat(last_exec)
        delta = timedelta(hours=routine["interval_hours"])

        if now - last_time >= delta:
            execute_routine(name, routine)

if __name__ == "__main__":
    check_triggers()
