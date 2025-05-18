# gpt_prompt_selector.py

import os
import json

INDEX_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/index.json"

def load_prompt_for_project(project_key=None, user_input=None):
    """
    Liefert den passenden Systemprompt auf Basis des Projekt-Keys oder des User-Inputs.
    """
    if not os.path.exists(INDEX_PATH):
        return "Handle im Stil der Gordon Holding. Professionell, klar, strukturiert."

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    # Versuche Projekt zu erkennen, wenn kein Key übergeben wurde
    if not project_key and user_input:
        project_key = resolve_project_key_from_text(user_input)

    project = index.get(project_key)
    if not project:
        return "Handle im Standard-GPT-Modus."

    return project.get("prompt_text", "Handle im Stil der Holding.")

def resolve_project_key_from_text(user_input):
    """
    Erkennt den passenden Projekt-Kontext auf Basis von Schlüsselwörtern in index.json
    """
    if not os.path.exists(INDEX_PATH):
        return "2.0_GORDON_HOLDING"

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    text = user_input.lower()

    for project_key, block in index.items():
        for keyword in block.get("keywords", []):
            if keyword.lower() in text:
                return project_key

    return "2.0_GORDON_HOLDING"  # Fallback für neutralen Business-Kontext
