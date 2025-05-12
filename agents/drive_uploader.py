import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Lokaler Pfad zu deinem JSON-Key im Projekt
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__),
    '../../0.1 Zugangsdaten/ai-zentrale-cloud-a825585d152f.json'
)

# Google Drive Zugriff einschränken auf: Dateien hochladen
SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# API-Client für Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(filepath, drive_folder_id=None):
    """
    Lädt eine Datei in Google Drive hoch.
    Optional kann eine Ziel-Folder-ID angegeben werden.
    """
    file_metadata = {'name': os.path.basename(filepath)}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    mime_type, _ = mimetypes.guess_type(filepath)
    media = MediaFileUpload(filepath, mimetype=mime_type)

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"✅ Datei '{uploaded_file['name']}' erfolgreich hochgeladen.")
    print(f"🔗 Öffnen: {uploaded_file['webViewLink']}")
    return uploaded_file
