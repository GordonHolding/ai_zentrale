"# modules/authentication/google_utils.py
# ⛓ Zugriff auf Google Drive via Service Account – optimiert für AI-ZENTRALE

import logging
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Versuche, log_interaction zu importieren. Falls das Modul fehlt, nimm Dummy-Funktion.
try:
    from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
except ImportError:
    def log_interaction(*args, **kwargs):
        pass

# 🔕 Google API Logging unterdrücken (nur echte Fehler anzeigen)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('google').setLevel(logging.ERROR)

# 🔐 Erstellt Credentials aus .json-Datei für beliebigen Account – direkt aus /etc/secrets
def get_service_account_credentials(account_name=""office_gordonholding"", scopes=None):
    try:
        scopes = scopes or []
        key_path = f""/etc/secrets/service_account_{account_name}.json""
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=scopes)
        return credentials
    except Exception as e:
        log_interaction(""System"", f""❌ Fehler bei Credentials für {account_name}"", str(e))
        raise e

# 📂 Google Drive-API zurückgeben
def get_drive_service(account_name=""office_gordonholding"", log_access=False):
    scopes = [""https://www.googleapis.com/auth/drive""]
    creds = get_service_account_credentials(account_name, scopes)
    if log_access:
        log_credential_usage(""Drive"", account_name)
    return build(""drive"", ""v3"", credentials=creds)

# 📊 Google Sheets-API zurückgeben
def get_sheet_service(account_name=""office_gordonholding"", log_access=False):
    scopes = [""https://www.googleapis.com/auth/spreadsheets""]
    creds = get_service_account_credentials(account_name, scopes)
    if log_access:
        log_credential_usage(""Sheets"", account_name)
    return build(""sheets"", ""v4"", credentials=creds)

# 🧠 Optionales DSGVO-kompatibles Log – nur wenn log_access=True gesetzt
def log_credential_usage(service_type, account_name):
    log_interaction(
        user=""System"",
        prompt=f""🔐 Google Zugriff: {service_type} via {account_name}"",
        response=""✅ Zugriff erfolgreich"",
        path=""memory_log.json""
    )"
