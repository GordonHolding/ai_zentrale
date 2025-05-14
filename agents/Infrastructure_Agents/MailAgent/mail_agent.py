# mail_agent.py

from gmail_auth import get_gmail_credentials
from googleapiclient.discovery import build
from mail_config import MAIL_ACCOUNTS, LABEL_RULES
from mail_triggers import apply_label, archive_message, save_draft

def process_emails(account_key):
    creds = get_gmail_credentials(MAIL_ACCOUNTS[account_key])
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", maxResults=20).execute()
    messages = results.get("messages", [])

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = msg_data.get("snippet", "").lower()

        for label, keywords in LABEL_RULES.items():
            if any(kw in snippet for kw in keywords):
                apply_label(service, msg["id"], label)

        if "entwurf" in snippet or "antwort folgt" in snippet:
            save_draft(service, msg["id"], "Vielen Dank – wir melden uns in Kürze!")

        if "archivieren" in snippet or "erledigt" in snippet:
            archive_message(service, msg["id"])

    print(f"✅ Verarbeitung abgeschlossen für: {account_key}")
