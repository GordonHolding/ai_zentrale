# Datei: memory_log_search.py

import json
import os

LOG_FILE = "memory_log.json"

def memory_log_search(criteria: str, entry_type: str = None, max_results: int = 10):
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE) as f:
        memory = json.load(f)

    results = []
    for entry in memory:
        if entry_type and entry.get("type") != entry_type:
            continue

        entry_text = json.dumps(entry).lower()
        if criteria.lower() in entry_text:
            results.append(entry)

        if len(results) >= max_results:
            break

    return results
