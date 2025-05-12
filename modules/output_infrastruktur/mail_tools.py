from modules.authentication.gmail_auth import get_gmail_credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def send_mail(recipient, subject, message_text, sender="me"):
    creds = get_gmail_credentials(["https://www.googleapis.com/auth/gmail.send"])
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(message_text)
    message["to"] = recipient
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw_message}

    sent = service.users().messages().send(userId=sender, body=body).execute()
    return f"E-Mail gesendet an {recipient} (ID: {sent['id']})"
