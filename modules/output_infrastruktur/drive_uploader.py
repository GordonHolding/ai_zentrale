from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from modules.google_utils import get_credentials
import os

def upload_to_drive(file_path, name=None, mime_type="application/pdf", folder_id=None):
    creds = get_credentials(["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": name or os.path.basename(file_path)}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")
