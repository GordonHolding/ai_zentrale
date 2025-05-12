from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def create_sheet(title: str):
    creds = get_credentials(["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().create(body={"properties": {"title": title}}).execute()
    return sheet["spreadsheetId"]
