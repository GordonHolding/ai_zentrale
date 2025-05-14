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

# Erweiterte Label-Regeln für automatische Klassifizierung
LABEL_RULES = {
    "finance": ["rechnung", "zahlung", "invoice", "überweisung", "kontostand", "gutschrift", "mahnung"],
    "events": ["einladung", "event", "veranstaltung", "termin", "konferenz", "meeting", "webinar"],
    "urgent": ["dringend", "sofort", "wichtig", "notfall", "unverzüglich"],
    "hr": ["bewerbung", "lebenslauf", "vorstellungsgespräch", "job", "karriere", "mitarbeiter", "kündigung"],
    "legal": ["vertrag", "agb", "datenschutz", "haftung", "rechtsanwalt", "gericht", "klage", "einspruch"],
    "sales": ["angebot", "anfrage", "deal", "kunde", "preis", "bestellung", "rabatt"],
    "marketing": ["kampagne", "newsletter", "promotion", "social media", "branding", "influencer"],
    "investor": ["beteiligung", "kapital", "pitch", "investment", "due diligence", "term sheet", "vc"],
    "tech": ["bug", "server", "system", "fehler", "debug", "entwickler", "repository", "update"],
    "personal": ["privat", "urlaub", "familie", "persönlich", "arzt", "versicherung"],
    "travel": ["flug", "hotel", "reise", "buchung", "reiseplan", "check-in", "boarding"],
    "default": []
}
