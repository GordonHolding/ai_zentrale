# drive_utils.py – Utility-Funktionen für den DriveAgent

import os
from googleapiclient.discovery import build
from modules.authentication.google_utils import get_drive_service

def move_file_or_folder(file_id, new_parent_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    result = service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
    return {"status": "moved", "file_id": file_id, "new_parent": new_parent_id}

def rename_file_or_folder(file_id, new_name, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    service.files().update(fileId=file_id, body={"name": new_name}).execute()
    return {"status": "renamed", "file_id": file_id, "new_name": new_name}

def find_files(query, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return response.get("files", [])

def summarize_folder(folder_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    query = f"'{folder_id}' in parents and trashed = false"
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = response.get("files", [])
    summary = {
        "total": len(files),
        "types": {}
    }
    for f in files:
        mime = f["mimeType"]
        summary["types"][mime] = summary["types"].get(mime, 0) + 1
    return summary

def extract_metadata(file_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    file = service.files().get(fileId=file_id, fields="id, name, mimeType, createdTime, modifiedTime, owners, size").execute()
    return file

def convert_file_to_pdf(file_id, export_mime="application/pdf", account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    result = service.files().export(fileId=file_id, mimeType=export_mime).execute()
    return {"status": "converted", "file_id": file_id, "mime": export_mime}

def check_permissions(file_id, account_name="office_gordonholding"):
    service = get_drive_service(account_name)
    permissions = service.permissions().list(fileId=file_id).execute()
    return permissions.get("permissions", [])
