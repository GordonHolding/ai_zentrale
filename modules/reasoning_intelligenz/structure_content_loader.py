# structure_content_loader.py
import os
import json

# Basispfad zur AI-Zentrale (lokal oder synchronisiert über Google Drive)
AI_ZENTRALE_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

# Mapping von JSON-Dateinamen zu ihrer Bedeutung
JSON_TITEL_MAPPING = {
    "00_masterstruktur_navigationslogik_ai_zentrale.json": "MASTERSTRUKTUR",
    "00_system_und_ki_basis.json": "SYSTEMBASIS",
    "10_privat_struktur.json": "PRIVATBEREICH",
    "20_gordon_holding_struktur.json": "GORDON HOLDING",
    "30_dresscode_struktur.json": "DRESSCODE",
    "40_tochter_struktur.json": "TOCHTERGESELLSCHAFTEN"
}


def load_structure_content(filename):
    """
    Lädt eine bestimmte Struktur-JSON-Datei anhand des Dateinamens.
    """
    path = os.path.join(AI_ZENTRALE_PATH, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden von {filename}: {e}")
        return {}


def get_all_structure_blocks():
    """
    Lädt alle bekannten .json Strukturdateien und gibt sie als Dict zurück.
    """
    result = {}
    for fname, label in JSON_TITEL_MAPPING.items():
        result[label] = load_structure_content(fname)
    return result


def search_structure(keyword):
    """
    Durchsucht alle Inhalte nach einem bestimmten Begriff.
    """
    results = []
    data = get_all_structure_blocks()
    for title, content in data.items():
        if keyword.lower() in json.dumps(content).lower():
            results.append(title)
    return results


def get_structure_section(title):
    """
    Gibt den Inhalt eines bestimmten Strukturblocks zurück.
    """
    filename = next((k for k, v in JSON_TITEL_MAPPING.items() if v == title), None)
    if filename:
        return load_structure_content(filename)
    return {}
