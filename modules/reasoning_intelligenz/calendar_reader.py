from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def list_calendar_events():
    creds = get_credentials(["https://www.googleapis.com/auth/calendar.readonly"])
    service = build("calendar", "v3", credentials=creds)
    events_result = service.events().list(
        calendarId="primary", maxResults=10, singleEvents=True, orderBy="startTime"
    ).execute()
    return events_result.get("items", [])
