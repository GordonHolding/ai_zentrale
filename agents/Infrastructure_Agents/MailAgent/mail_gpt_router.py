# mail_gpt_router.py – GPT-Routing für E-Mail-Entscheidungen

import openai
from agents.Infrastructure_Agents.MailAgent.mail_agent_prompt import MAIL_AGENT_SYSTEM_PROMPT
from mail_triggers import (
    archive_message, mark_as_read, apply_label,
    save_draft, extract_attachments
)

def route_gpt_decision(snippet, service, msg_data):
    """
    Fragt GPT, wie eine bestimmte Mail verarbeitet werden soll,
    und ruft die entsprechende Funktion auf.
    """

    try:
        msg_id = msg_data["id"]
        headers = msg_data["payload"].get("headers", [])
        internal_date = int(msg_data.get("internalDate", 0))  # UNIX-Timestamp (ms)
        label_ids = msg_data.get("labelIds", [])
        thread_id = msg_data.get("threadId", "")
        
        # Header extrahieren
        def get_header(name):
            for h in headers:
                if h["name"].lower() == name.lower():
                    return h["value"]
            return ""

        subject = get_header("Subject")
        sender = get_header("From")
        date = get_header("Date")

        # GPT ansprechen
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

        # Entscheidung umsetzen
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

        print(f"🧠 GPT-Routing abgeschlossen: {gpt_reply}")

    except Exception as e:
        print(f"❌ GPT-Routing-Fehler: {e}")
