def generate_sheet(title, headers):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        "0.0 SYSTEM/0.1 Zugangsdaten/ai-zentrale-cloud-....json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    body = {
        "properties": {"title": title},
        "sheets": [{"properties": {"title": "Tabelle1"}}]
    }
    sheet = service.spreadsheets().create(body=body).execute()
    sheet_id = sheet["spreadsheetId"]
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Tabelle1!A1",
        valueInputOption="RAW",
        body={"values": [headers]}
    ).execute()
    return sheet_id
