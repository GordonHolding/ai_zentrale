# trigger_prompt_loader.py

import json
import os

PROMPT_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/trigger_prompts.json"

def load_prompt_for_trigger(trigger_key):
    if not os.path.exists(PROMPT_PATH):
        return {
            "system": "Standardrolle: Führe diesen Trigger aus.",
            "format": "Standardantwortformat."
        }

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        prompts = json.load(f)
        return prompts.get(trigger_key, {
            "system": "Standardrolle: Führe diesen Trigger aus.",
            "format": "Standardantwortformat."
        })
