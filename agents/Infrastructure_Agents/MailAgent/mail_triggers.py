# mail_triggers.py

def apply_label(service, msg_id, label_name):
    label_id = ensure_label_exists(service, label_name)
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"addLabelIds": [label_id]}
    ).execute()

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

def save_draft(service, msg_id, reply_text):
    original = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
    thread_id = original.get("threadId")

    message_body = {
        "message": {
            "raw": "",  # Optional: MIME-Code mit reply
            "threadId": thread_id
        }
    }

    service.users().drafts().create(userId="me", body=message_body).execute()

def archive_message(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["INBOX"]}
    ).execute()
