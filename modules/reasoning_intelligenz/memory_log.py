def log_interaction(user, prompt, response):
    import json, os
    path = "memory_log.json"
    memory = []
    if os.path.exists(path):
        with open(path) as f:
            memory = json.load(f)
    memory.append({"user": user, "prompt": prompt, "response": response})
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)
