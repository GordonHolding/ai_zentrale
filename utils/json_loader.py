# json_loader.py – Optimierter GDrive Loader für ai_zentrale
# 🚀 Semantische Pfade + ID-Cache als Hauptverfahren, rekursive Suche als Fallback
# ⚡ Deutlich schneller durch intelligentes Caching und Pfadauflösung

import io
import json
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload
from modules.authentication.google_utils import get_drive_service

# --------------------------------------------
# 🔧 ID-Cache laden aus zentraler JSON-Datenbank
# --------------------------------------------
def load_index():
    """
    Lädt die zentrale Indexdatei json_file_index.json mit Drive-IDs und semantischen Pfaden.
    """
    try:
        service = get_drive_service()
        file_id = "1-IgxnWWmEdTBL0x-0_wcyn9JJBMhUBoO"  # ID der json_file_index.json
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        return json.load(fh)
    except Exception as e:
        print(f"[IndexLoader] Fehler beim Laden des Index: {e}")
        return {}

# --------------------------------------------
# 🔍 Hauptmethode: Lädt Datei per ID-Cache oder rekursiv
# --------------------------------------------
def load_json_from_gdrive(filename: str) -> dict:
    """
    Lädt eine JSON-Datei aus Google Drive mit semantischer Pfadauflösung (ID-Cache).
    Falls nicht im Index gefunden, erfolgt eine langsame, rekursive Suche als Fallback.
    """
    service = get_drive_service()
    index = load_index()

    # 🔎 Suche Datei im Index (rekursiv über JSON-Struktur)
    def recursive_search(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, dict) and val.get("path", "").endswith(filename):
                    return val
                result = recursive_search(val)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = recursive_search(item)
                if result:
                    return result
        return None

    meta = recursive_search(index)
    file_id = meta.get("drive_id") if meta else None

    # 🔁 Fallback: Rekursive Google Drive-Suche
    if not file_id:
        print(f"[Fallback] Datei '{filename}' nicht im Index gefunden. Starte Suche...")
        try:
            query = f"name = '{filename}' and trashed = false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])
            if files:
                file_id = files[0]["id"]
            else:
                return {"error": f"Datei '{filename}' nicht in Drive gefunden."}
        except Exception as e:
            return {"error": f"Fehler bei GDrive-Suche: {e}"}

    # 📥 Dateiinhalt laden
    try:
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

# --------------------------------------------
# 🛡️ checked_load_json: Mit expliziter Fehlerprüfung
# --------------------------------------------
def checked_load_json(filename: str, context_hint: str = "") -> dict:
    """
    Lädt eine JSON-Datei und prüft auf Fehler.
    Löst eine RuntimeError aus, wenn Fehler enthalten oder Datei leer/unlesbar.
    Ideal für Debugging und sichere Ladeprozesse.
    """
    data = load_json_from_gdrive(filename)
    if not isinstance(data, dict) or "error" in data:
        raise RuntimeError(
            f"Fehler beim Laden von '{context_hint or filename}': {data.get('error') if isinstance(data, dict) else 'Unbekannter Fehler'}"
        )
    return data

# --------------------------------------------
# 🔁 safe_load_json: Fehlerresistent, ohne Abbruch
# --------------------------------------------
def safe_load_json(filename: str) -> dict:
    """
    Wie load_json_from_gdrive, aber gibt immer ein Dict zurück – auch bei Fehlern.
    Bricht nie ab. Ideal für optionale Dateien wie Logs oder Templates.
    """
    try:
        return load_json_from_gdrive(filename)
    except Exception as e:
        return {"error": str(e)}

# --------------------------------------------
# 🚫 Schreibschutz – kein Speichern erlaubt
# --------------------------------------------
def write_json(*args, **kwargs):
    """
    Schreibvorgänge sind deaktiviert (GDrive-only-Modus).
    """
    raise NotImplementedError("Schreiben von JSON ist deaktiviert (GDrive-only).")

# --------------------------------------------
# 🔁 Alias-Funktionen für Kompatibilität (optional)
# --------------------------------------------
load_json = load_json_from_gdrive  # frühere Standardfunktion in Modulen
# checked_load_json → für sichere Prozesse mit Exception
# safe_load_json → für sanftes Handling ohne Crash
