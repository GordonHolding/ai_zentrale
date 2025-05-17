# gpt_prompt_selector.py

import json
import os

INDEX_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/index.json"

def load_prompt_for_project(project_key):
    if not os.path.exists(INDEX_PATH):
        return "Handle im Stil der Gordon Holding. Professionell, klar, strukturiert."

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    project = index.get(project_key)
    if not project:
        return "Handle im Standard-GPT-Modus."

    return project.get("prompt_text", "Handle im Stil der Holding.")
