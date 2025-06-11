# json_loader.py – GDrive-only Loader für AI-ZENTRALE
# ⛓ Lädt JSONs direkt aus Google Drive per Service Account
# 🔁 Mit Alias-Funktionen für GPT-Kompatibilität & Robustheit

import io
import json
from googleapiclient.http import MediaIoBaseDownload
from modules.authentication.google_utils import get_drive_service


def find_file_id_recursive(filename: str, parent_id: str = 'root') -> str:
    """
    Sucht rekursiv nach einer Datei mit dem angegebenen Namen im gesamten Google Drive (ab parent_id).
    Gibt die erste gefundene File-ID zurück oder None.
    """
    service = get_drive_service()
    query = f"name = '{filename}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, parents)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    return None


def load_json_from_gdrive(filename: str) -> dict:
    """
    Lädt eine JSON-Datei von Google Drive, indem sie rekursiv nach dem Namen sucht.
    Gibt ein Dictionary zurück oder ein dict mit 'error'-Key.
    """
    try:
        file_id = find_file_id_recursive(filename)
        if not file_id:
            return {"error": f"Datei '{filename}' nicht in Google Drive gefunden."}
        service = get_drive_service()
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        return json.load(fh)
    except Exception as e:
        return {"error": f"Fehler beim Laden von '{filename}': {e}"}


# -----------------------------------------------------
# 🔁 GPT-kompatible Alias-Funktionen für universelle Nutzung
# -----------------------------------------------------

# Standard-Import für alle Module
load_json = load_json_from_gdrive

# Schreibvorgänge sind in dieser Version deaktiviert (GDrive-API ist read-only im Loader)
def write_json(*args, **kwargs):
    raise NotImplementedError("Schreiben von JSON ist in dieser GDrive-Version nicht aktiviert.")


# -----------------------------------------------------
# 🛡️ Optionale Zusatzfunktion: Fehlergeprüftes Laden
# -----------------------------------------------------

def safe_load_json(filename: str) -> dict:
    """
    Lädt JSON sicher, gibt bei Fehlern leeres dict + .get("error") zurück.
    """
    result = load_json(filename)
    if not isinstance(result, dict):
        return {"error": f"Ungültiges Format in Datei '{filename}'"}
    return result


def checked_load_json(filename: str, context_hint: str = "") -> dict:
    """
    Wirft eine Exception bei Ladefehlern – für kritische Systemmodule (z. B. GPTAgent)
    """
    result = load_json(filename)
    if not isinstance(result, dict) or "error" in result:
        error_msg = result.get("error") if isinstance(result, dict) else "Unbekannter Fehler"
        raise RuntimeError(f"❌ Fehler beim Laden von '{context_hint or filename}': {error_msg}")
    return result
