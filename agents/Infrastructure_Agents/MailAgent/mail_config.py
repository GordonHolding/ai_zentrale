# mail_config.py – Konfiguration

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

# Keywords zur automatischen Kategorisierung
LABEL_RULES = {
    "finance": ["rechnung", "zahlung", "invoice"],
    "events": ["einladung", "event", "veranstaltung"],
    "urgent": ["dringend", "sofort", "wichtig"],
    "default": []
}
