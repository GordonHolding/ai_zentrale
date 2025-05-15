import os

# Basispfad des MailAgent-Verzeichnisses auf Google Drive
MAIL_AGENT_BASE_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.2 Agenten/Infrastructure_Agents/MailAgent"

# SCOPES für Gmail-Zugriff
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.metadata"
]

# Gmail-Konten (Mapping zu OAuth-Credentials)
MAIL_ACCOUNTS = {
    "office": "office_gordonholding",
    "business": "business_barrygordon",
    "private": "gordonmunich"
}

# Pfade zu Tokens und Client-Secrets
TOKEN_PATHS = {
    "office": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "token_office_gordonholding.json"),
    "business": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "token_business_barrygordon.json")
}

CLIENT_SECRETS = {
    "office": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "client_secret_office_gordonholding.json"),
    "business": os.path.join(MAIL_AGENT_BASE_PATH, "tokens", "client_secret_business_barrygordon.json")
}

# Systemprompt-Pfad (aus Google Drive)
MAIL_AGENT_PROMPT_PATH = os.path.join(
    MAIL_AGENT_BASE_PATH,
    "MailAgent_Kontexte_Promptweitergaben",
    "mail_agent_prompt.json"
)

def load_mail_agent_prompt():
    with open(MAIL_AGENT_PROMPT_PATH) as f:
        return f.read()

# Lokale Logs
MAIL_ROUTING_LOG = os.path.join(MAIL_AGENT_BASE_PATH, "MailAgent_Memory", "mail_routing_log.json")
MAIL_ERROR_LOG = os.path.join(MAIL_AGENT_BASE_PATH, "MailAgent_Memory", "mail_error_log.json")

# Automatische Label-Regeln
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
