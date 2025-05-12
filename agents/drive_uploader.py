from google.oauth2 import service_account
from googleapiclient.discovery import build
import mimetypes
import os

# Pfad zur JSON-Datei (angepasst!)
SERVICE_ACCOUNT_FILE = '0.0 SYSTEM & KI-GRUNDBASIS/0.1 Zugangsdaten/ai-zentrale-cloud-a825585d152f.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(filepath, drive_folder_id=None):
    file_metadata = {'name': os.path.basename(filepath)}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    mime_type, _ = mimetypes.guess_type(filepath)
    media = {'mimeType': mime_type or 'application/octet-stream', 'body': open(filepath, 'rb')}

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()

    print(f"✅ Datei '{uploaded_file['name']}' hochgeladen:")
    print(f"🔗 Link: {uploaded_file['webViewLink']}")
    return uploaded_file

# Testaufruf (nur wenn direkt ausgeführt)
if __name__ == '__main__':
    upload_file_to_drive('beispiel.pdf')
