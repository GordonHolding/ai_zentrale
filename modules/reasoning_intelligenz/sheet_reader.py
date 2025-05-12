from google.oauth2 import service_account
from googleapiclient.discovery import build

def read_sheet(spreadsheet_id, range_name):
    creds = service_account.Credentials.from_service_account_file(
        "0.0 SYSTEM/0.1 Zugangsdaten/ai-zentrale-cloud-....json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return sheet.get("values", [])
