# json_config.py – Dynamische JSON-Verwaltung über zentralen Index

from utils.json_loader import load_json

# 🔁 Lädt vollständigen Index aller verwaltbaren JSON-Dateien
def get_json_index():
    data = load_json("json_memory_index.json")
    if isinstance(data, dict):
        return data
    return {}

# 🔎 Gibt die Pfadinfo zu einer spezifischen Datei anhand des Schlüssels zurück
def get_json_config(file_key):
    index = get_json_index()
    return index.get(file_key, None)
