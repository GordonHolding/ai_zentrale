# watcher_trigger_runner.py

from agents.Infrastructure_Agents.TriggerAgent.watcher_trigger import scan_drive_and_trigger
from datetime import datetime

if __name__ == "__main__":
    result = scan_drive_and_trigger()
    print(f"[{datetime.now().isoformat()}] WATCHER_TRIGGER → {result}")
