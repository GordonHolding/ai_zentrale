import openai
from mail_triggers import (
    archive_message, mark_as_read, apply_label,
    save_draft, extract_attachments, detect_iban,
    extract_pdf_attachments, sender_prioritization,
    log_email_to_memory
)
from mail_config import load_mail_agent_prompt

MAIL_AGENT_SYSTEM_PROMPT = load_mail_agent_prompt()

def route_gpt_decision(snippet, service, msg_data):
    try:
        msg_id = msg_data["id"]
        headers = msg_data["payload"].get("headers", [])
        internal_date = int(msg_data.get("internalDate", 0))  # UNIX-Timestamp (ms)
        label_ids = msg_data.get("labelIds", [])
        thread_id = msg_data.get("threadId", "")

        def get_header(name):
            for h in headers:
                if h["name"].lower() == name.lower():
                    return h["value"]
            return ""

        subject = get_header("Subject")
        sender = get_header("From")
        date = get_header("Date")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": MAIL_AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": f"""
Hier ist eine neue E-Mail:

📨 Betreff: {subject}
📬 Von: {sender}
📅 Datum: {date}
🕑 Timestamp: {internal_date}
🏷️ Labels: {label_ids}
🧵 Thread: {thread_id}

📎 Vorschau:
{snippet}

Was soll ich tun? (z. B. Label, Archiv, Antwort, Anhang speichern, markieren, löschen)
"""}
            ]
        )

        gpt_reply = response.choices[0].message["content"].lower()

        if "archivieren" in gpt_reply or "archive" in gpt_reply:
            archive_message(service, msg_id)

        if "label" in gpt_reply:
            apply_label(service, msg_data)

        if "entwurf" in gpt_reply or "antwort" in gpt_reply or "draft" in gpt_reply:
            save_draft(service, msg_data, "Vielen Dank für Ihre Nachricht. Wir melden uns zeitnah.")

        if "gelesen" in gpt_reply or "read" in gpt_reply:
            mark_as_read(service, msg_id)

        if "anhang" in gpt_reply or "attachment" in gpt_reply:
            extract_attachments(service, msg_data)

        if detect_iban(msg_data):
            apply_label(service, msg_data)

        pdfs = extract_pdf_attachments(msg_data)
        if pdfs:
            print(f"📄 PDF-Anhänge erkannt: {len(pdfs)} Dateien")

        sender_prioritization(service, msg_data)

        log_email_to_memory(msg_data, category="unclassified", summary=gpt_reply[:200])

        print(f"🧠 GPT-Routing abgeschlossen: {gpt_reply}")

    except Exception as e:
        print(f"❌ GPT-Routing-Fehler: {e}")
