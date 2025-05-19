import re
from mail_config import LABEL_RULES
from memory_log import log_mail_entry

VIP_SENDERS = [
    "hepp@kanzlei.de",
    "florian@investor.ag",
    "barry@private.gmbh"
]

def archive_message(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["INBOX"]}
    ).execute()

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()

def apply_label(service, message, label_override=None):
    snippet = message.get("snippet", "").lower()
    label = label_override if label_override else "default"
    if not label_override:
        for key, keywords in LABEL_RULES.items():
            if any(kw in snippet for kw in keywords):
                label = key
                break
    label_id = ensure_label_exists(service, label)
    service.users().messages().modify(
        userId="me",
        id=message["id"],
        body={"addLabelIds": [label_id]}
    ).execute()
    return label

def ensure_label_exists(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]
    new_label = service.users().labels().create(
        userId="me",
        body={"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    ).execute()
    return new_label["id"]

def save_draft(service, message, body_text):
    thread_id = message.get("threadId")
    draft_body = {
        "message": {
            "threadId": thread_id,
            "raw": ""  # Optional: MIME-formatieren
        }
    }
    service.users().drafts().create(userId="me", body=draft_body).execute()

def delete_message(service, msg_id):
    service.users().messages().delete(userId="me", id=msg_id).execute()

def get_threads(service, message):
    thread_id = message.get("threadId")
    thread = service.users().threads().get(userId="me", id=thread_id).execute()
    return thread.get("messages", [])

def summarize_thread(thread_messages):
    content = "\n".join([msg.get("snippet", "") for msg in thread_messages])
    return f"Zusammenfassung: {content[:300]}..."

def send_email_reply(service, message, body_text):
    print(f"[GPT-Antwort] Entwurf vorbereitet für: {message['id']}\nInhalt: {body_text}")

def extract_attachments(service, message):
    parts = message.get("payload", {}).get("parts", [])
    for part in parts:
        if part.get("filename") and "attachmentId" in part.get("body", {}):
            print(f"📎 Anhang erkannt: {part['filename']}")

def extract_pdf_attachments(message):
    pdf_files = []
    parts = message.get("payload", {}).get("parts", [])
    for part in parts:
        filename = part.get("filename", "")
        if filename.lower().endswith(".pdf") and "attachmentId" in part.get("body", {}):
            print(f"📄 PDF-Anhang erkannt: {filename}")
            pdf_files.append(filename)
    return pdf_files

def detect_iban(message):
    snippet = message.get("snippet", "")
    body_parts = message.get("payload", {}).get("parts", [])
    full_text = snippet
    for part in body_parts:
        data = part.get("body", {}).get("data", "")
        full_text += " " + data
    iban_pattern = r"\bDE\d{20}\b"
    match = re.search(iban_pattern, full_text.replace(" ", "").replace("\n", ""))
    if match:
        print(f"🏦 IBAN erkannt: {match.group()}")
        return True
    return False

def sender_prioritization(service, message):
    headers = message.get("payload", {}).get("headers", [])
    sender = ""
    for h in headers:
        if h["name"].lower() == "from":
            sender = h["value"]
            break
    if any(vip.lower() in sender.lower() for vip in VIP_SENDERS):
        print(f"🚨 VIP-Absender erkannt: {sender}")
        apply_label(service, message, label_override="urgent")

def log_email_to_memory(message, category, summary):
    headers = message.get("payload", {}).get("headers", [])
    subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "Kein Betreff")
    sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unbekannt")
    internal_date = int(message.get("internalDate", 0))
    mail_id = message.get("id", "")
    log_mail_entry(mail_id, sender, subject, category, summary)
