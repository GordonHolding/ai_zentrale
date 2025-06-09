# json_loader.py – Zentrale JSON-Verwaltung für AI-ZENTRALE (lokal + Google Drive)

import os
import json
import io
from googleapiclient.http import MediaIoBaseDownload
from modules.authentication.google_utils import get_drive_service

# 🗂️ Lokales Root-Verzeichnis (für Entwicklungsumgebung)
CONFIG_DIR = os.getenv("CONFIG_DIR") or "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale"

# 🔄 JSON-Datei laden – zuerst lokal, dann aus Google Drive
def load_json(filename: str) -> dict:
    try:
        # 🔍 Lokale Suche
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                path = os.path.join(root, filename)
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)

        # ☁️ Fallback: Aus Google Drive laden
        return load_json_from_drive(filename)

    except Exception as e:
        return {"error": f"❌ Fehler beim JSON-Laden: {e}"}

# 💾 JSON-Datei schreiben (nur lokal)
def write_json(filename: str, data: dict) -> dict:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            if filename in files:
                path = os.path.join(root, filename)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return {"success": f"✅ Datei '{filename}' erfolgreich aktualisiert."}
        return {"error": f"📂 Datei '{filename}' nicht gefunden zum Schreiben."}
    except Exception as e:
        return {"error": f"❌ Fehler beim Schreiben von '{filename}': {e}"}

# 📁 Liste aller .json-Dateien lokal
def list_all_configs(extension: str = ".json") -> list:
    result = []
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(extension):
                    result.append(os.path.join(root, file))
        return result
    except Exception as e:
        return [f"❌ Fehler beim Auflisten der JSON-Dateien: {e}"]

# 🔍 Suche erste lokale Datei mit Keyword im Namen
def get_json_by_keyword(keyword: str) -> dict:
    try:
        for root, _, files in os.walk(CONFIG_DIR):
            for file in files:
                if file.endswith(".json") and keyword.lower() in file.lower():
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
        return {"error": f"🔍 Keine passende Datei mit Keyword '{keyword}' gefunden."}
    except Exception as e:
        return {"error": f"❌ Fehler beim JSON-Zugriff mit Keyword: {e}"}

# ☁️ JSON aus Google Drive laden (Backup-Strategie)
def load_json_from_drive(filename: str) -> dict:
    try:
        service = get_drive_service()
        query = f"name = '{filename}' and mimeType = 'application/json'"
        results = service.files().list(q=query, fields="files(id)").execute()
        files = results.get("files", [])
        if not files:
            return {"error": f"📂 Datei '{filename}' nicht in Google Drive gefunden."}

        file_id = files[0]["id"]
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        return json.load(fh)
    except Exception as e:
        return {"error": f"❌ Fehler beim Drive-Zugriff für '{filename}': {e}"}
