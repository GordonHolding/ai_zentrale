import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

openai.api_key = os.getenv("OPENAI_API_KEY")

# Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen bei deiner AI-Zentrale, Barry. Ich bin bereit.")

# Antwort auf jede Nachricht
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # GPT-3.5 Anfrage
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist eine strategische KI-Zentrale für Barry Gordon, CEO einer Holding."},
            {"role": "user", "content": user_input}
        ]
    )

    # Antwort senden
    await update.message.reply_text(response.choices[0].message.content)

# Bot starten
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot läuft...")
    app.run_polling()
