# json_protection.py – setzt und überprüft Schreibschutz für sensible Dateien

from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_config

# 📦 Liste geschützter Schlüssel (kann später aus eigener JSON-Datei geladen werden)
PROTECTED_FILES = [
    "system_identity_prompt",
    "json_validation_rules",
    "json_protection_rules",
    "json_revision_history",
    "00_ai_zentrale_masterstruktur",
    "00_system_ki_basis"
]

# 🔐 Prüft, ob eine Datei geschützt ist
def is_protected(file_key: str) -> bool:
    return file_key in PROTECTED_FILES

# 🔐 Gibt Schutzstatus als GPT-lesbare Info zurück
def protection_status(file_key: str) -> str:
    if is_protected(file_key):
        return f"🔒 Die Datei '{file_key}' ist schreibgeschützt."
    else:
        return f"✏️ Die Datei '{file_key}' ist bearbeitbar."

# 🛑 Verhindert unautorisierte Änderung – Rückgabe für Steuerung in anderen Modulen
def block_if_protected(file_key: str) -> dict:
    if is_protected(file_key):
        return {
            "error": f"❌ Änderung an '{file_key}' wurde blockiert – Schreibschutz aktiv."
        }
    return {"allowed": True}
