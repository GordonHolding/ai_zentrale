from googleapiclient.discovery import build
from modules.google_utils import get_credentials
import datetime

def create_event(summary, start_time, end_time, calendar_id="primary"):
    creds = get_credentials(["https://www.googleapis.com/auth/calendar"])
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Europe/Berlin"},
        "end": {"dateTime": end_time, "timeZone": "Europe/Berlin"},
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event.get("htmlLink")
