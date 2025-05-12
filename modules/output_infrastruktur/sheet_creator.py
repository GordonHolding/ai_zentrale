def create_sheet(title: str):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        "0.0 SYSTEM/0.1 Zugangsdaten/ai-zentrale-cloud-....json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().create(body={"properties": {"title": title}}).execute()
    return sheet["spreadsheetId"]
