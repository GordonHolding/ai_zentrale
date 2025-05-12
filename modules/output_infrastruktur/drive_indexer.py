from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def index_drive(folder_id=None):
    creds = get_credentials(["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get("files", [])
