# structure_content_loader.py

import os
import json

STRUCTURE_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/"
INDEX_PATH = os.path.join(STRUCTURE_DIR, "index.json")

def load_structure(project_key):
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    project = index.get(project_key)
    if not project:
        return {}

    structure_file = project.get("structure_file")
    structure_path = os.path.join(STRUCTURE_DIR, structure_file)

    if os.path.exists(structure_path):
        with open(structure_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_all_structures():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    result = {}
    for key, block in index.items():
        structure_file = block.get("structure_file")
        path = os.path.join(STRUCTURE_DIR, structure_file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                result[key] = json.load(f)
    return result
