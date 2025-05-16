# telegram_bot.py – mit Tracker, Verlauf & Upload-Analyse

import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from modules.reasoning_intelligenz.conversation_tracker import log_and_get_context, add_gpt_reply
from modules.input_interfaces.telegram_file_handler import handle_file

openai.api_key = os.getenv("OPENAI_API_KEY")

# /start Begrüßung
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen in der AI-Zentrale. Was möchtest du tun?")

# Textnachricht analysieren & Verlauf berücksichtigen
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = str(update.effective_user.id)
    print(f"📩 Telegram Input: {user_input}")

    try:
        messages = log_and_get_context(user_id, user_input)

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        add_gpt_reply(user_id, reply)

        await update.message.reply_text(reply)

    except Exception as e:
        print(f"❌ Fehler: {e}")
        await update.message.reply_text(f"❌ Systemfehler: {e}")

# Bot starten
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    print("📲 Telegram Bot läuft…")
    app.run_polling()
