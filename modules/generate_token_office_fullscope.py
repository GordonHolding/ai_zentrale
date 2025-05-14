from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Maximale Gmail-Scopes – für vollständige Kontrolle per AI
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.metadata"
]

def main():
    # Richtiger Dateiname für deinen neuen Desktop-OAuth-Client
    creds_path = os.path.expanduser("~/Desktop/client_secret_office_gordonholding.json")

    # OAuth-Flow starten
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=8000)

    # Token speichern – sauber benannt
    token_path = os.path.expanduser("~/Desktop/token_office_at_gordonholding.json")
    with open(token_path, "w") as token:
        token.write(creds.to_json())

    print(f"✅ Token erfolgreich gespeichert unter:\n{token_path}")

if __name__ == "__main__":
    main()
