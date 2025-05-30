# json_formatter.py – sorgt für automatisches Format nach jeder Änderung

import json

# 🧹 Formatierung mit Einrückung & UTF-8-Encoding
def format_json(data: dict, indent: int = 2) -> str:
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as e:
        return f"❌ Fehler beim Formatieren: {e}"

# 💾 Speichert formatierte JSON-Datei
def save_formatted_json(file_path: str, data: dict) -> dict:
    try:
        formatted = format_json(data)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted)
        return {"success": f"✅ JSON gespeichert und formatiert → {file_path}"}
    except Exception as e:
        return {"error": f"❌ Fehler beim Speichern von '{file_path}': {e}"}
