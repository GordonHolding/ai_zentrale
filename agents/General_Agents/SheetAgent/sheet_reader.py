# sheet_reader.py

from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def read_sheet(spreadsheet_id, range_name):
    creds = get_credentials(["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    return sheet.get("values", [])
