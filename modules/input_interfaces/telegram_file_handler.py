# telegram_file_handler.py – Dateiannahme für Telegram + GPT-Logik

import os
import datetime
from telegram import Update
from telegram.ext import ContextTypes

from modules.output_infrastruktur.file_uploader import save_uploaded_file
from modules.reasoning_intelligenz.conversation_tracker import attach_file_summary
from modules.ai_intelligenz.gpt_vision_handler import analyze_image
from modules.ai_intelligenz.gpt_pdf_summary import summarize_pdf

UPLOAD_DIR = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History/Uploads"

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    file = update.message.document or update.message.photo[-1] if update.message.photo else None

    if not file:
        await update.message.reply_text("❌ Kein unterstützter Dateityp erkannt.")
        return

    # Dateiname + temporärer Pfad
    file_name = file.file_name if hasattr(file, "file_name") else f"photo_{datetime.datetime.now().timestamp()}.jpg"
    file_path = os.path.join("/tmp", file_name)
    tg_file = await file.get_file()
    await tg_file.download_to_drive(file_path)

    # Datei speichern + Memory verknüpfen
    save_uploaded_file(
        user_id=user_id,
        file_path=file_path,
        original_filename=file_name,
        description="Upload via Telegram-Bot"
    )

    await update.message.reply_text(f"📎 Datei empfangen: {file_name}")

    # 🧠 Bildanalyse
    if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        await update.message.reply_text("🧠 Bild erkannt – GPT Vision wird gestartet...")
        result = analyze_image(file_path)
        attach_file_summary(user_id, result)
        await update.message.reply_text(result)

    # 📄 PDF-Zusammenfassung
    elif file_name.lower().endswith(".pdf"):
        await update.message.reply_text("📄 PDF erkannt – wird analysiert...")
        result = summarize_pdf(file_path)
        attach_file_summary(user_id, result)
        await update.message.reply_text(result)
