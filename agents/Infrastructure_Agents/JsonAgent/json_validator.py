# json_validator.py – prüft JSON-Inhalte gegen Validierungsregeln

from utils.json_loader import load_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_index

# 🔍 Validiert eine komplette Datei anhand definierter Regeln
def validate_json(file_key: str, content: dict = None) -> dict:
    rules = load_json("json_validation_rules.json")
    file_config = get_json_index().get(file_key)
    if not file_config:
        return {"status": "error", "message": f"Keine Konfiguration für '{file_key}' gefunden."}
    
    filename = file_config["filename"]
    file_rules = rules.get(filename)
    if not file_rules:
        return {"status": "warning", "message": f"Keine Regeln definiert für '{filename}'."}
    
    if content is None:
        content = load_json(filename)
    if not isinstance(content, dict):
        return {"status": "error", "message": f"Inhalt von '{filename}' ist kein dict."}
    
    missing_keys = []
    for key in file_rules.get("required_keys", []):
        if key not in content:
            missing_keys.append(key)

    if missing_keys:
        return {
            "status": "fail",
            "message": f"Fehlende Schlüssel in '{filename}': {', '.join(missing_keys)}",
            "missing": missing_keys
        }

    return {
        "status": "pass",
        "message": f"✅ '{filename}' erfüllt alle Validierungsregeln."
    }

# 🔍 Validiert einen einzelnen Schlüssel-Wert-Eintrag für eine Datei
def validate_entry(file_key: str, key: str, value) -> dict:
    rules = load_json("json_validation_rules.json")
    file_config = get_json_index().get(file_key)

    if not file_config:
        return {"status": "error", "message": f"Keine Konfiguration für '{file_key}' gefunden."}

    filename = file_config["filename"]
    file_rules = rules.get(filename, {})

    required_keys = file_rules.get("required_keys", [])
    encoding = file_rules.get("encoding", "utf-8")

    if key not in required_keys:
        return {
            "status": "warning",
            "message": f"'{key}' ist nicht in den definierten required_keys für '{filename}' enthalten."
        }

    # Weitere Checks wären hier möglich: Datentyp, Format etc.
    return {
        "status": "valid",
        "message": f"'{key}' ist ein gültiger Eintrag für '{filename}' mit Encoding '{encoding}'."
    }
