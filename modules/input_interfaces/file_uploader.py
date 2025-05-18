# file_uploader.py

import os
import shutil
from datetime import datetime
from modules.reasoning_intelligenz.memory_log import log_interaction
from modules.reasoning_intelligenz.vision_tools import analyze_image
from modules.reasoning_intelligenz.pdf_tools import summarize_pdf_with_gpt

UPLOAD_FOLDER = "uploads/"

def save_uploaded_file(user_id, file_path, original_filename, description=""):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{timestamp}__{original_filename}"
    user_dir = os.path.join(UPLOAD_FOLDER, user_id)

    os.makedirs(user_dir, exist_ok=True)
    target_path = os.path.join(user_dir, filename)

    shutil.copy(file_path, target_path)

    # Memory-Log
    log_upload_event(user_id, target_path, description)

    # Automatische GPT-Analyse
    attach_file_summary(target_path, user_id)

def log_upload_event(user_id, file_path, description):
    entry = {
        "type": "Upload",
        "path": file_path,
        "user": user_id,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }
    log_interaction(user_id, entry)

def attach_file_summary(file_path, user_id):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        summary = analyze_image(file_path)
    elif ext in [".pdf"]:
        summary = summarize_pdf_with_gpt(file_path)
    else:
        summary = f"📁 Datei gespeichert: {file_path}"

    result = {
        "type": "FileSummary",
        "summary": summary,
        "source": os.path.basename(file_path),
        "timestamp": datetime.now().isoformat()
    }
    log_interaction(user_id, result)
