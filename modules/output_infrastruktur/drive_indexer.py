def index_drive(folder_id=None):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        "0.0 SYSTEM/0.1 Zugangsdaten/ai-zentrale-cloud-....json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get("files", [])
