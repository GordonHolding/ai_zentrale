# mail_agent.py – Hauptlogik

from gmail_auth import get_gmail_credentials
from googleapiclient.discovery import build
from mail_config import MAIL_ACCOUNTS
from mail_triggers import (
    archive_message, mark_as_read, apply_label,
    save_draft, delete_message, get_threads,
    summarize_thread, send_email_reply
)
from agents.Infrastructure_Agents.MailAgent.mail_agent_prompt import MAIL_AGENT_SYSTEM_PROMPT

def process_emails(account_key):
    creds = get_gmail_credentials(MAIL_ACCOUNTS[account_key])
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=10).execute()
    messages = results.get("messages", [])

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        msg_id = msg_data["id"]

        # Beispielhafte Nutzung:
        mark_as_read(service, msg_id)
        label = apply_label(service, msg_data)
        archive_message(service, msg_id)
        save_draft(service, msg_data, "Vielen Dank für Ihre Nachricht. Wir melden uns zeitnah.")
        threads = get_threads(service, msg_data)
        summary = summarize_thread(threads)
        send_email_reply(service, msg_data, summary)

    print(f"✅ Verarbeitung abgeschlossen für: {account_key}")
