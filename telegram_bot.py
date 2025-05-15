# Datei: telegram_bot.py

import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from agents.Infrastructure_Agents.RouterAgent.router_agent import handle_user_input

openai.api_key = os.getenv("OPENAI_API_KEY")

# /start Begrüßung
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen in der AI-Zentrale. Was möchtest du tun?")

# Hauptlogik: Eingabe analysieren, RouterAgent aktivieren
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(f"📩 Telegram Input: {user_input}")

    try:
        result = handle_user_input(user_input)
        await update.message.reply_text(f"🤖 RouterAgent: {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler bei der Verarbeitung: {e}")

# Start des Telegram-Bots
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("📲 Telegram Bot läuft...")
    app.run_polling()
