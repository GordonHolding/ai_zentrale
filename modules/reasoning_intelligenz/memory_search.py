def search_memory(keyword):
    import json
    with open("memory_log.json") as f:
        memory = json.load(f)
    return [entry for entry in memory if keyword in entry["prompt"] or keyword in entry["response"]]
