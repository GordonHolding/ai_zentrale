# trigger_triggers.py – GPT-basierte Triggererkennung und Auslösung

from datetime import datetime
from utils.json_loader import load_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_trigger_execution

# 🔄 Lade GPT-Trigger-Konfiguration aus JSON (z. B. trigger_gpt_config.json)
def load_gpt_trigger_config():
    config = load_json("trigger_gpt_config.json")
    if "error" in config:
        return {}
    return config.get("gpt_triggers", {})

# 🧠 Erkenne GPT-Trigger in einem eingegebenen Text
def check_gpt_trigger(user_input: str) -> list:
    trigger_config = load_gpt_trigger_config()
    matched_triggers = []

    for phrase, trigger_name in trigger_config.items():
        if phrase.lower() in user_input.lower():
            matched_triggers.append({
                "type": "gpt_trigger",
                "name": trigger_name,
                "source": "gpt_input",
                "matched_on": phrase,
                "timestamp": datetime.utcnow().isoformat()
            })

    if matched_triggers:
        log_trigger_execution("GPT-Trigger", [t["name"] for t in matched_triggers], datetime.utcnow().isoformat())

    return matched_triggers

# ▶ Direktes Testing
if __name__ == "__main__":
    test_input = "bitte cleanup jetzt und drive analysieren"
    results = check_gpt_trigger(test_input)
    for r in results:
        print(f"✅ Trigger erkannt: {r['name']} durch Phrase: '{r['matched_on']}'")
