# gpt_prompt_selector.py

import os
import json

PROMPT_MAP_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/prompt_map.json"
PROMPT_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Prompts/"

def load_prompt_map():
    if os.path.exists(PROMPT_MAP_PATH):
        with open(PROMPT_MAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_prompt(prompt_key):
    prompt_map = load_prompt_map()
    file_name = prompt_map.get(prompt_key)

    if not file_name:
        return "Du bist eine GPT-Instanz der Gordon Holding. Handle professionell und strukturiert."

    full_path = os.path.join(PROMPT_DIR, file_name)
    if not os.path.exists(full_path):
        return f"[Fehler: Prompt-Datei {file_name} nicht gefunden]"

    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
