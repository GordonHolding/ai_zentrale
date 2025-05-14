# mail_gpt_router.py – KI-Routing für E-Mail-Entscheidungen

import openai
from agents.Infrastructure_Agents.MailAgent.mail_agent_prompt import MAIL_AGENT_SYSTEM_PROMPT
from mail_triggers import archive_message, mark_as_read, apply_label, save_draft


def route_gpt_decision(snippet, service, msg_data):
    """
    Fragt GPT, wie eine bestimmte Mail verarbeitet werden soll,
    und ruft die entsprechende Funktion auf.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": MAIL_AGENT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Hier ist eine neue Mail:

{snippet}

Was soll ich tun? (Label, Archiv, Antwort etc.)"}
            ]
        )
        gpt_reply = response.choices[0].message["content"].lower()

        # Ausgabe analysieren und passende Aktion durchführen
        msg_id = msg_data["id"]

        if "archivieren" in gpt_reply:
            archive_message(service, msg_id)
        if "label" in gpt_reply:
            apply_label(service, msg_data)
        if "entwurf" in gpt_reply or "antwort" in gpt_reply:
            save_draft(service, msg_data, "Vielen Dank für Ihre Nachricht. Wir melden uns zeitnah.")
        if "gelesen" in gpt_reply:
            mark_as_read(service, msg_id)

        print(f"🧠 GPT-Routing abgeschlossen: {gpt_reply}")

    except Exception as e:
        print(f"❌ GPT-Routing-Fehler: {e}")
