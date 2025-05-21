# memory_log_search.py

import os
import json
from typing import List, Dict

MEMORY_BASE_PATH = "0.2 Agenten"

def collect_memory_files() -> List[str]:
    """
    Sammelt alle .json-Dateien aus *_Memory/ Ordnern in allen Agentenstrukturen.
    """
    collected = []
    for root, dirs, files in os.walk(MEMORY_BASE_PATH):
        if "_Memory" in root:
            for file in files:
                if file.endswith(".json"):
                    collected.append(os.path.join(root, file))
    return collected

def memory_log_search(criteria: str) -> List[Dict]:
    """
    Durchsucht alle Memory-Files nach dem Kriterium (Text-Snippet).
    """
    results = []
    files = collect_memory_files()

    if not files:
        return [{"result": "⚠️ Keine Memory-Dateien gefunden."}]

    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                memory = json.load(f)
                for entry in memory:
                    entry_text = " ".join([
                        str(entry.get("prompt", "")),
                        str(entry.get("response", "")),
                        str(entry.get("summary", "")),
                        str(entry.get("subject", "")),
                        str(entry.get("category", "")),
                        str(entry.get("type", ""))
                    ]).lower()

                    if criteria.lower() in entry_text:
                        result_entry = dict(entry)
                        result_entry["source"] = path
                        results.append(result_entry)
        except:
            continue

    if not results:
        return [{"result": f"❌ Keine Einträge gefunden für: '{criteria}'"}]

    return results
