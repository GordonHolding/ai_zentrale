# trigger_triggers.py – GPT-basierte Triggererkennung und zentrale Triggersteuerung

from datetime import datetime
from utils.json_loader import load_json
from agents.Infrastructure_Agents.TriggerAgent.trigger_utils import log_trigger_execution
from agents.Infrastructure_Agents.TriggerAgent.time_trigger import check_time_trigger
from agents.Infrastructure_Agents.TriggerAgent.custom_action import check_custom_trigger
from agents.Infrastructure_Agents.TriggerAgent.watcher_trigger import check_watcher_trigger

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

# ▶ Hauptfunktion zum Ausführen aller aktiven Trigger
def run_all_triggers(config: dict) -> list:
    results = []

    # 1. Zeitbasierte Trigger
    try:
        results.extend(check_time_trigger(config))
    except Exception as e:
        print(f"⚠️ Fehler in check_time_trigger: {e}")

    # 2. Benutzerdefinierte Aktionen
    try:
        results.extend(check_custom_trigger(config))
    except Exception as e:
        print(f"⚠️ Fehler in check_custom_trigger: {e}")

    # 3. Dateiüberwachung / Watcher
    try:
        results.extend(check_watcher_trigger(config))
    except Exception as e:
        print(f"⚠️ Fehler in check_watcher_trigger: {e}")

    # 4. GPT-Trigger basierend auf Benutzereingabe
    user_input = config.get("sample_input", "")
    if user_input:
        try:
            results.extend(check_gpt_trigger(user_input))
        except Exception as e:
            print(f"⚠️ Fehler in check_gpt_trigger: {e}")

    return results

# ▶ Direktes Testing
if __name__ == "__main__":
    test_config = {
        "sample_input": "bitte cleanup jetzt und drive analysieren"
    }
    output = run_all_triggers(test_config)
    for entry in output:
        print(f"✅ Trigger erkannt: {entry['name']} ({entry['type']})")
