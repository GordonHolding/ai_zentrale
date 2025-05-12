from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def generate_sheet(title, headers):
    creds = get_credentials(["https://www.googleapis.com/auth/spreadsheets"])
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
