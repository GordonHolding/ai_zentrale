# watcher_trigger.py – Erkennt neue oder geänderte Strukturblöcke im gesamten AI-Zentrale Ordner

import os
import json
from modules.reasoning_intelligenz.structure_content_loader import get_all_structure_blocks
from agents.Infrastructure_Agents.WatcherTrigger.watcher_trigger_log import log_trigger_event
from agents.General_Agents.AgentSuggester.agent_suggester import suggest_agents_for_structure

LATEST_INDEX = "memory_logs/latest_structure_index.json"

def scan_and_trigger():
    current = get_all_structure_blocks()
    if not os.path.exists(LATEST_INDEX):
        with open(LATEST_INDEX, "w") as f:
            json.dump(current, f, indent=2)
        return

    with open(LATEST_INDEX, "r") as f:
        previous = json.load(f)

    new_entries = [entry for entry in current if entry not in previous]

    if new_entries:
        log_trigger_event(new_entries)
        suggest_agents_for_structure()
        with open(LATEST_INDEX, "w") as f:
            json.dump(current, f, indent=2)
