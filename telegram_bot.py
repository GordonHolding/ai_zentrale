import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# API-Schlüssel aus Umgebungsvariablen
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Logging für Fehlersuche
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Barry, ich bin dein AI-Interface. Wie kann ich Dir helfen?")

# GPT-Antwortlogik
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist eine strategische, strukturierte KI für Barry Gordon, CEO einer Holding."},
            {"role": "user", "content": user_input},
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# Main App starten
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot läuft...")
    app.run_polling()
