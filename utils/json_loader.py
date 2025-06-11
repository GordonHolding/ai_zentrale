# json_loader.py – Nur Google Drive – AI-ZENTRALE optimiert

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
# 🔁 Alias-Funktionen für GPT-/Legacy-Kompatibilität
# -----------------------------------------------------

load_json = load_json_from_gdrive

def write_json(*args, **kwargs):
    """
    Placeholder: Schreibvorgänge sind in dieser Version deaktiviert oder extern geregelt.
    """
    raise NotImplementedError("Schreiben von JSON ist in GDrive-only-Version nicht aktiviert.")
