# json_validator.py – prüft JSON-Inhalte gegen Validierungsregeln

from utils.json_loader import load_json
from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_index

# 🔍 Validiert eine Datei anhand definierter Regeln
def validate_json(file_key: str, content: dict = None) -> dict:
    rules = load_json("json_validation_rules.json")
    file_config = get_json_index().get(file_key)
    if not file_config:
        return {"status": "error", "message": f"Keine Konfiguration für '{file_key}' gefunden."}
    
    filename = file_config["filename"]
    file_rules = rules.get(filename)
    if not file_rules:
        return {"status": "warning", "message": f"Keine Regeln definiert für '{filename}'."}
    
    # Inhalt laden, falls nicht übergeben
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
