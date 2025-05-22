import os
import json
import openai
from modules.output_infrastruktur.document_template_engine import generate_document_from_template
from modules.output_infrastruktur.mail_tools import send_mail

TEMPLATES_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/reply_templates.json"
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_templates():
    if os.path.exists(TEMPLATES_PATH):
        with open(TEMPLATES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_reply(template_key, replacements, fallback_text=None):
    templates = load_templates()
    config = templates.get(template_key)

    if config and config.get("type") == "gdoc":
        return generate_document_from_template(
            doc_id=config["doc_id"],
            placeholders=config["placeholders"],
            replacements=replacements
        )

    elif fallback_text:
        return fallback_text.format(**replacements)

    else:
        return "❌ Keine gültige Vorlage gefunden."

def generate_template_text(template_type):
    templates = {
        "nda": "Dies ist eine Vertraulichkeitsvereinbarung zwischen [NAME] und [UNTERNEHMEN], gültig ab [DATUM].",
        "kuendigung": "Hiermit kündige ich fristgerecht zum [KÜNDIGUNGSDATUM] meinen Vertrag bei [UNTERNEHMEN]."
    }
    return templates.get(template_type.lower(), "Vorlage nicht gefunden.")

def send_template_reply(template_key, recipient, replacements, fallback_text=None, subject=None, mail_mode="save_draft_confirm"):
    """
    Sendet oder speichert eine E-Mail basierend auf einer Vorlage (Text oder GDoc).
    """
    reply = generate_reply(template_key, replacements, fallback_text)
    message_text = reply if isinstance(reply, str) else str(reply)

    # Optional: subject aus replacements ableiten
    subject = subject or replacements.get("BETREFF", "Antwort")

    return send_mail(
        recipient=recipient,
        subject=subject,
        message_text=message_text,
        html_text=f"<p>{message_text}</p>",
        attachments=None,
        mail_mode=mail_mode
    )
