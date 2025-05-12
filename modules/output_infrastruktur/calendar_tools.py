def create_event(summary, start_time, end_time, calendar_id="primary"):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    import datetime

    creds = service_account.Credentials.from_service_account_file(
        "0.0 SYSTEM/0.1 Zugangsdaten/ai-zentrale-cloud-....json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Europe/Berlin"},
        "end": {"dateTime": end_time, "timeZone": "Europe/Berlin"},
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event.get("htmlLink")
