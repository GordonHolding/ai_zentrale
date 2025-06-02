# watcher_trigger_runner.py

from agents.Infrastructure_Agents.TriggerAgent.watcher_trigger import scan_drive_and_trigger

if __name__ == "__main__":
    result = scan_drive_and_trigger()
    print(f"[WATCHER_TRIGGER] {result}")
