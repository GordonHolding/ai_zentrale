# calendar_reader.py – liest Fristen aus allen _Memory JSON-Dateien

import os
import json
from datetime import datetime

MEMORY_BASE_PATH = "agents/Infrastructure_Agents"

def find_all_memory_files():
    memory_files = []
    for agent in os.listdir(MEMORY_BASE_PATH):
        sub_path = os.path.join(MEMORY_BASE_PATH, agent)
        if os.path.isdir(sub_path):
            memory_dir = os.path.join(sub_path, f"{agent}_Memory")
            if os.path.isdir(memory_dir):
                for f in os.listdir(memory_dir):
                    if f.endswith(".json"):
                        memory_files.append(os.path.join(memory_dir, f))
    return memory_files

def extract_deadlines_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        deadlines = []
        for key, entry in data.items():
            if isinstance(entry, dict) and "due_date" in entry:
                deadlines.append({
                    "key": key,
                    "due_date": entry["due_date"],
                    "source": file_path
                })
        return deadlines
    except Exception:
        return []

def get_all_deadlines():
    files = find_all_memory_files()
    all_deadlines = []
    for f in files:
        all_deadlines.extend(extract_deadlines_from_json(f))
    return all_deadlines
