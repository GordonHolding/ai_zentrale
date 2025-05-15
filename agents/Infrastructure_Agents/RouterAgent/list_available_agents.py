# list_available_agents.py

import json
import os

REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__),
    "Router_Memory",
    "agent_registry.json"
)

def list_available_agents():
    try:
        with open(REGISTRY_PATH) as f:
            agents = json.load(f)
        print("🧠 Verfügbare Agenten:")
        for key, info in agents.items():
            print(f"• {info['name']} – {info['description']} [Status: {info['status']}]")
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Agentenübersicht: {e}")
