# drive_config.py – Zentrale Konfiguration für DriveAgent & Trigger

import os
import json

# 📁 Standardpfad zur Drive-Konfigurationsdatei
CONFIG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/drive_index_config.json"

# 🧠 Fallback-Werte (wenn JSON fehlt oder unvollständig)
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

# 📦 Konfiguration laden (mit Fallback)
def load_drive_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
        except Exception:
            pass
    return DEFAULT_CONFIG

# 🔁 Konfigurationswerte direkt bereitstellen
CONFIG = load_drive_config()
ROOT_FOLDER_ID = CONFIG["root_folder_id"]
ALLOWED_MIME_TYPES = CONFIG["allowed_mime_types"]
INCLUDE_ALL_MIME_TYPES = CONFIG["include_all_mime_types"]
IGNORE_FOLDERS = CONFIG["ignore_folders"]
LOG_TO_MEMORY = CONFIG["log_to_memory"]
ACCOUNT_NAME = CONFIG["account_name"]
