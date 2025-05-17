# gpt_response_parser.py

import json
import os

AGENT_REGISTRY_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/agent_registry.json"

def load_agent_registry():
    if os.path.exists(AGENT_REGISTRY_PATH):
        with open(AGENT_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def parse_gpt_response(text):
    """
    Sucht JSON-ähnliche Blöcke in einer GPT-Antwort und prüft auf bekannte Agenten.
    """
    try:
        # Rohtext extrahieren (z. B. aus ```json ... ```)
        raw_json = text.strip()
        if "```json" in raw_json:
            raw_json = raw_json.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_json:
            raw_json = raw_json.split("```")[1].strip()

        data = json.loads(raw_json)
        registry = load_agent_registry()

        agent_key = data.get("agent")
        if agent_key not in registry:
            return {
                "valid": False,
                "reason": f"Agent '{agent_key}' nicht registriert.",
                "raw": data
            }

        return {
            "valid": True,
            "action": data.get("action"),
            "agent": agent_key,
            "status": data.get("status", "unknown"),
            "raw": data
        }

    except Exception as e:
        return {
            "valid": False,
            "reason": f"Fehler beim Parsen: {str(e)}",
            "raw": text
        }
