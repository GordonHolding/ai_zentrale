# drive_indexer.py – Konfigurierbarer Drive-Scanner mit GPT-Zusammenfassung

import json
import os
from googleapiclient.discovery import build
from modules.authentication.google_utils import get_service_account_credentials
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from datetime import datetime

CONFIG_PATH = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/drive_index_config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def index_drive_from_config():
    config = load_config()
    return index_drive(
        folder_id=config["root_folder_id"],
        allowed_types=config.get("allowed_mime_types"),
        ignore_folders=config.get("ignore_folders", []),
        log_to_memory=config.get("log_to_memory", False),
        account_name=config.get("account_name", "office_gordonholding")
    )

def index_drive(folder_id, allowed_types=None, ignore_folders=None, log_to_memory=False, account_name="office_gordonholding"):
    creds = get_service_account_credentials(account_name, scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    def _scan(fid, path=""):
        results = []
        query = f"'{fid}' in parents and trashed = false"
        response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()

        for file in response.get("files", []):
            if file["mimeType"] == "application/vnd.google-apps.folder":
                if file["name"] in ignore_folders:
                    continue
                results.extend(_scan(file["id"], path + "/" + file["name"]))
            else:
                if allowed_types and file["mimeType"] not in allowed_types:
                    continue
                results.append({
                    "id": file["id"],
                    "name": file["name"],
                    "mimeType": file["mimeType"],
                    "path": path + "/" + file["name"]
                })
        return results

    files = _scan(folder_id)

    if log_to_memory:
        log_interaction("System", {
            "type": "DriveIndex",
            "files_found": len(files),
            "timestamp": datetime.now().isoformat()
        })

    return files

def drive_index_summary():
    files = index_drive_from_config()
    if not files:
        return "📁 Es wurden keine Dateien im Drive gefunden."

    text = f"📁 Es wurden {len(files)} Dateien im Drive gefunden:\n\n"
    for f in files[:10]:
        text += f"- {f['name']} ({f['mimeType']}) in {f['path']}\n"
    if len(files) > 10:
        text += f"... und {len(files) - 10} weitere."
    return text
