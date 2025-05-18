# file_uploader.py

import os
import shutil
import datetime
from modules.reasoning_intelligenz.memory_log import log_interaction
from modules.ai_intelligenz.gpt_vision_handler import analyze_image
from modules.ai_intelligenz.gpt_pdf_summary import summarize_pdf

UPLOAD_DIR = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History/Uploads"

def save_uploaded_file(user_id: str, file_path: str, original_filename: str, description: str):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f"{timestamp}__{original_filename}"
    full_target_path = os.path.join(UPLOAD_DIR, filename)
    shutil.copy(file_path, full_target_path)

    log_upload_event(user_id, full_target_path, description)
    attach_file_summary(full_target_path, user_id)

def log_upload_event(user_id, file_path, description):
    entry = {
        "type": "Upload",
        "path": file_path,
        "user": user_id,
        "description": description,
        "timestamp": datetime.datetime.now().isoformat()
    }
    log_interaction(user_id, entry)

def attach_file_summary(file_path, user_id):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        summary = analyze_image(file_path)
    elif ext in [".pdf"]:
        summary = summarize_pdf(file_path)
    else:
        summary = f"📁 Datei gespeichert: {file_path}"

    log_interaction(user_id, {
        "type": "FileSummary",
        "summary": summary,
        "source": os.path.basename(file_path),
        "timestamp": datetime.datetime.now().isoformat()
    })
