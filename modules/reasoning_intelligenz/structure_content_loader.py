# structure_content_loader.py – Strukturmodule via index.json laden

from utils.json_loader import load_json

def get_all_structures():
    index_data = load_json("index.json")
    structure_files = {}
    for entry in index_data.get("structure_files", []):
        file = entry.get("filename")
        key = entry.get("key") or file.replace(".json", "")
        structure_files[key] = load_json(file)
    return structure_files
