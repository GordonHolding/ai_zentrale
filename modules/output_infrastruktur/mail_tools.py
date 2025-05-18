from modules.authentication.gmail_auth import get_gmail_credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os

from modules.reasoning_intelligenz.memory_log import log_mail_entry


def send_mail(
    recipient,
    subject,
    message_text,
    html_text=None,
    attachments=None,
    sender="me",
    mail_mode="send_now"
):
    """
    Versendet eine E-Mail oder erstellt einen Entwurf basierend auf mail_mode.
    mail_mode = "send_now" | "save_draft_confirm" | "save_draft_prepare"
    """
    creds = get_gmail_credentials(["https://www.googleapis.com/auth/gmail.send"])
    service = build("gmail", "v1", credentials=creds)

    # MIME-Nachricht aufbauen
    message = MIMEMultipart("alternative")
    message["to"] = recipient
    message["subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    if html_text:
        message.attach(MIMEText(html_text, "html"))

    # Anhänge hinzufügen
    if attachments:
        for filepath in attachments:
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{os.path.basename(filepath)}"'
                    )
                    message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw_message}

    if mail_mode == "send_now":
        sent = service.users().messages().send(userId=sender, body=body).execute()
        log_mail_entry(
            mail_id=sent["id"],
            sender="system@gpt.ai",
            subject=subject,
            category="mail_sent",
            summary=message_text[:200]
        )
        return f"📤 Mail an {recipient} wurde gesendet (ID: {sent['id']})"

    elif mail_mode in ["save_draft_confirm", "save_draft_prepare"]:
        draft = service.users().drafts().create(
            userId=sender,
            body={"message": body}
        ).execute()

        log_mail_entry(
            mail_id=draft["id"],
            sender="system@gpt.ai",
            subject=subject,
            category="mail_draft",
            summary=f"{message_text[:200]}",
        )

        if mail_mode == "save_draft_confirm":
            return f"📥 Entwurf erstellt und wartet auf deine Bestätigung. (ID: {draft['id']})"
        else:
            return f"📝 Entwurf vorbereitet – liegt in Gmail bereit. (ID: {draft['id']})"

    else:
        return "❌ Ungültiger Modus für Mailversand."
