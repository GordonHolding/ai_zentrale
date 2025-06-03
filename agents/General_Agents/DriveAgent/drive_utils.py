# drive_utils.py – Utility-Funktionen für den DriveAgent

import io
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from modules.authentication.google_utils import get_drive_service

# 🔐 Schutz: JSON-Dateien sind geschützt – nur JsonAgent darf diese verändern
def protect_json_operations(file_name: str):
    if file_name and file_name.endswith(".json"):
        raise PermissionError("🚫 JSON-Dateien dürfen ausschließlich vom JsonAgent bearbeitet werden.")

# 🔁 Datei oder Ordner verschieben
def move_file_or_folder(file_id, new_parent_id, file_name=None, account_name="office_gordonholding"):
    protect_json_operations(file_name)
    service = get_drive_service(account_name)
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents', []))
    result = service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
    return {"status": "moved", "file_id": file_id, "new_parent": new_parent_id}

# 📝 Umbenennen von Datei oder Ordner
def rename_file_or_folder(file_id, new_name, account_name="office_gordonholding"):
    protect_json_operations(new_name)
    service = get_drive_service(account_name)
    service.files().update(fileId=file_id, body={"name": new_name}).execute()
    return {"status": "renamed", "file_id": file_id, "new_name": new_name}

# 🔍 Suche nach Datei(en) per Query
def find_files(query, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return response.get("files", [])

# 📂 Inhalt eines Ordners als Liste (Basisfunktion)
def list_files_in_folder(folder_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    query = f"'{folder_id}' in parents and trashed = false"
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return response.get("files", [])

# 📦 Zusammenfassung von Dateitypen in Ordnern
def summarize_folder(folder_id, account_name="office_gordonholding"):
    files = list_files_in_folder(folder_id, account_name)
    summary = {
        "total": len(files),
        "types": {}
    }
    for f in files:
        mime = f.get("mimeType", "unknown")
        summary["types"][mime] = summary["types"].get(mime, 0) + 1
    return summary

# 🧾 Extrahiere strukturierte Metadaten für Datei
def extract_metadata(file_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    file = service.files().get(
        fileId=file_id,
        fields="id, name, mimeType, createdTime, modifiedTime, owners, size"
    ).execute()
    return file

# 📤 Konvertiere Datei nach PDF (Google Docs only)
def convert_file_to_pdf(file_id, export_mime="application/pdf", account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    result = service.files().export(fileId=file_id, mimeType=export_mime).execute()
    return {"status": "converted", "file_id": file_id, "mime": export_mime}

# 🔐 Rechte anzeigen (für Governance-Checks)
def check_permissions(file_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    permissions = service.permissions().list(fileId=file_id).execute()
    return permissions.get("permissions", [])

# 🧠 JSON-Array-Datei aktualisieren (Eintrag anhängen)
def append_entry_to_drive_json(file_path: str, entry: dict, account_name="office_gordonholding"):
    service = get_drive_service(account_name)

    # Datei-ID suchen
    query = f"name = '{os.path.basename(file_path)}' and trashed = false"
    response = service.files().list(q=query, fields="files(id, name)").execute()
    items = response.get("files", [])
    if not items:
        raise FileNotFoundError(f"📂 Datei nicht gefunden: {file_path}")
    file_id = items[0]["id"]

    # Herunterladen
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)

    # Bestehende Daten einlesen
    try:
        data = json.load(fh)
    except Exception:
        data = []

    # Nur JSON-Arrays erlaubt
    if not isinstance(data, list):
        raise ValueError("🚫 Dateiinhalt ist kein JSON-Array.")

    # Neuen Eintrag hinzufügen
    data.append(entry)
    updated_content = io.BytesIO(json.dumps(data, indent=2).encode("utf-8"))
    media = MediaIoBaseUpload(updated_content, mimetype="application/json")
    service.files().update(fileId=file_id, media_body=media).execute()

    return {"status": "saved", "file": file_path, "entries_total": len(data)}
