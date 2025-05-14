# mail_config.py

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.metadata"
]

MAIL_ACCOUNTS = {
    "office": "office_gordonholding",
    "business": "business_barrygordon",
    "private": "gordonmunich"
}

# Filter-Keywords für Auto-Sortierung
LABEL_RULES = {
    "invoice": ["rechnung", "payment", "überweisung", "invoice"],
    "event": ["einladung", "event", "party", "gala"],
    "urgent": ["dringend", "sofort", "!!!", "wichtig"],
    "marketing": ["newsletter", "angebot", "promo"]
}
