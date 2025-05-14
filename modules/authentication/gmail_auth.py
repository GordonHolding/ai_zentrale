import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Alle Scopes – einheitlich systemweit
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.metadata"
]

def get_gmail_credentials(account_name="office_gordonholding"):
    base_path = "/etc/secrets"

    token_path = os.path.join(base_path, f"token_{account_name}.json")
    client_path = os.path.join(base_path, f"client_secret_{account_name}.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        with open(client_path, "r") as f:
            creds_data = json.load(f)
        flow = InstalledAppFlow.from_client_config(creds_data, scopes=SCOPES)
        creds = flow.run_local_server(port=8000)
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds
