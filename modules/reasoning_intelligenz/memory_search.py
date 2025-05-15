def search_memory(keyword):
    import json
    with open("memory_log.json") as f:
        memory = json.load(f)
    return [
        entry for entry in memory
        if keyword.lower() in str(entry.get("prompt", "")).lower()
        or keyword.lower() in str(entry.get("response", "")).lower()
        or keyword.lower() in str(entry.get("summary", "")).lower()
        or keyword.lower() in str(entry.get("subject", "")).lower()
    ]
