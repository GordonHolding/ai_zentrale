import os
import json

# Pfade dynamisch definieren (für Memory & Index)
MEMORY_PATH = "agents/Infrastructure_Agents/MemoryAgent/MemoryAgent_Memory/memory_log.json"
INDEX_PATH = "agents/Infrastructure_Agents/MemoryAgent/MemoryAgent_Memory/memory_index.json"

def create_if_missing():
    """
    Erstellt Standard-Dateien, falls sie noch nicht existieren.
    """
    for path in [MEMORY_PATH, INDEX_PATH]:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump([], f, indent=2)
            print(f"📁 Erstellt: {path}")
        else:
            print(f"✅ Bereits vorhanden: {path}")

def read_memory():
    with open(MEMORY_PATH) as f:
        return json.load(f)

def search_memory(keyword):
    memory = read_memory()
    return [
        entry for entry in memory
        if keyword.lower() in json.dumps(entry).lower()
    ]

def add_memory_entry(entry: dict):
    memory = read_memory()
    memory.append(entry)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
    print("✅ Eintrag gespeichert.")

# Beispielhafte Initialisierung bei Direktausführung
if __name__ == "__main__":
    create_if_missing()
