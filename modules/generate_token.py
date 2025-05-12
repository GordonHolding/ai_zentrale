from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes je nach Bedarf anpassen
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def main():
    creds_path = "0.0 SYSTEM/0.1 Zugangsdaten/client_secret_1046247609064-0fe5dsec75u6bu73n306keu267a1qrcl.apps.googleusercontent.com.json"  # Pfad zur JSON-Datei anpassen!
    
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=8000)

    # Speichere Token lokal ab
    with open("token.json", "w") as token:
        token.write(creds.to_json())

if __name__ == "__main__":
    main()
