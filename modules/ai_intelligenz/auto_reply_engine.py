# auto_reply_engine.py

import os
import json
import openai
from modules.output_infrastruktur.document_template_engine import generate_document_from_template

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
