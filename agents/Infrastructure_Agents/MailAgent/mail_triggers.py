# mail_triggers.py – Helferfunktionen

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

def apply_label(service, message):
    snippet = message.get("snippet", "").lower()
    label = "default"

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
