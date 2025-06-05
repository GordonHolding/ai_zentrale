# list_available_agents.py

from utils.json_loader import load_json

def list_available_agents():
    registry = load_json("agent_registry.json")
    print("\n📦 Verfügbare Agenten:\n")

    for key, data in registry.items():
        if data.get("active", False):
            label = data.get("label", "Kein Label")
            desc = data.get("description", "Keine Beschreibung")
            print(f"– {key} → {label}: {desc}")

if __name__ == "__main__":
    list_available_agents()

