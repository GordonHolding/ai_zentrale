from googleapiclient.discovery import build
from modules.google_utils import get_credentials

def read_latest_emails(user_id="me", max_results=5):
    creds = get_credentials(["https://www.googleapis.com/auth/gmail.readonly"])
    service = build("gmail", "v1", credentials=creds)

    # Liste der letzten E-Mails
    results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId=user_id, id=msg["id"]).execute()
        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(kein Betreff)")
        emails.append(subject)

    return emails
