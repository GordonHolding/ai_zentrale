# trigger_runner.py

from modules.reasoning_intelligenz.time_based_trigger_checker import check_and_execute_triggers

if __name__ == "__main__":
    results = check_and_execute_triggers()
    for r in results:
        print(f"[TRIGGER] {r}")
