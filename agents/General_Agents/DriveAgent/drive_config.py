# drive_config.py – Zentrale Konfiguration für DriveAgent & Trigger

from utils.json_loader import load_json

# 📄 Drive-Konfigurationsdatei (Dateiname – Pfad wird automatisch im json_loader gesucht)
CONFIG_FILENAME = "drive_index_config.json"

# 🧠 Fallback-Werte (werden automatisch ergänzt, falls im JSON unvollständig oder fehlerhaft)
DEFAULT_CONFIG = {
    "root_folder_id": "root",
    "allowed_mime_types": [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.google-apps.document",
        "application/vnd.google-apps.spreadsheet"
    ],
    "include_all_mime_types": False,
    "ignore_folders": [],
    "log_to_memory": False,
    "account_name": "office_gordonholding"
}

# 🧩 JSON laden + Fallback-Merge
CONFIG = load_json(CONFIG_FILENAME)
if not isinstance(CONFIG, dict) or "root_folder_id" not in CONFIG:
    CONFIG = DEFAULT_CONFIG
else:
    CONFIG = {**DEFAULT_CONFIG, **CONFIG}

# 🔁 Direkt verwendbare Konfig-Variablen (für alle Module)
ROOT_FOLDER_ID = CONFIG["root_folder_id"]
ALLOWED_MIME_TYPES = CONFIG["allowed_mime_types"]
INCLUDE_ALL_MIME_TYPES = CONFIG["include_all_mime_types"]
IGNORE_FOLDERS = CONFIG["ignore_folders"]
LOG_TO_MEMORY = CONFIG["log_to_memory"]
ACCOUNT_NAME = CONFIG["account_name"]
