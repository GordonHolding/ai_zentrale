import os

# Basispfad für alles, was MailAgent lokal speichert
MAIL_AGENT_BASE_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.2 Agenten/Infrastructure_Agents/MailAgent"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.metadata"
]

# Gmail-Konten
MAIL_ACCOUNTS = {
    "office": "office_gordonholding",
    "business": "business_barrygordon",
    "private": "gordonmunich"
}

# Token- und Secret-Dateien
TOKEN_PATHS = {
    "office": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "token_office_gordonholding.json"),
    "business": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "token_business_barrygordon.json")
}

CLIENT_SECRETS = {
    "office": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "client_secret_office_gordonholding.json"),
    "business": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "client_secret_business_barrygordon.json")
}

# Lokale Logs (Memory-ähnlich, aber nur für Aktionen)
MAIL_ROUTING_LOG = os.path.join(MAIL_AGENT_BASE_PATH, "MailAgent_Memory", "mail_routing_log.json")
MAIL_ERROR_LOG = os.path.join(MAIL_AGENT_BASE_PATH, "MailAgent_Memory", "mail_error_log.json")

# Automatische Label-Regeln (nutzt apply_label())
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
