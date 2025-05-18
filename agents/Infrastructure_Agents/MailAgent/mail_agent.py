from mail_config import MAIL_ACCOUNTS
from mail_gpt_router import route_gpt_decision
from modules.authentication.gmail_auth import get_gmail_credentials
from googleapiclient.discovery import build

def process_emails(account_key):
    creds = get_gmail_credentials(MAIL_ACCOUNTS[account_key])
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=10).execute()
    messages = results.get("messages", [])

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = msg_data.get("snippet", "")
        route_gpt_decision(snippet, service, msg_data)

    print(f"✅ GPT-MailAgent abgeschlossen für: {account_key}")
