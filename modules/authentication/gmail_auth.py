import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

def get_gmail_credentials():
    with open("/etc/secrets/gmail_oauth.json", "r") as f:
        creds_data = json.load(f)

    flow = InstalledAppFlow.from_client_config(
        creds_data,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"]
    )

    creds = flow.run_local_server(port=8000)
    return creds
