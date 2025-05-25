# modules/authentication/google_utils.py

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# 🔐 Zentrale Service Account-Funktion
def get_service_account_credentials(account_name="office_gordonholding", scopes=[]):
    base_path = os.getenv("GOOGLE_SECRET_PATH", "/etc/secrets")
    key_path = os.path.join(base_path, f"service_account_{account_name}.json")
    return service_account.Credentials.from_service_account_file(key_path, scopes=scopes)

# 📂 Bonus: Google Drive Objekt direkt zurückgeben
def get_drive_service(account_name="office_gordonholding", log_access=False):
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = get_service_account_credentials(account_name, scopes)
    if log_access:
        log_credential_usage("Drive", account_name)
    return build("drive", "v3", credentials=creds)

# 📊 Bonus: Google Sheets Objekt zurückgeben
def get_sheet_service(account_name="office_gordonholding", log_access=False):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = get_service_account_credentials(account_name, scopes)
    if log_access:
        log_credential_usage("Sheets", account_name)
    return build("sheets", "v4", credentials=creds)

# 🧠 Loggt, wann welches Google-System genutzt wurde (für GPT & DSGVO)
def log_credential_usage(service_type, account_name):
    log_interaction("System", f"Google Zugriff: {service_type} über Account {account_name}", "✅ Zugriff erfolgreich")

get_credentials = get_service_account_credentials
