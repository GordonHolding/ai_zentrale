import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# API-Schlüssel
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Barry, ich bin dein Telegram-GPT. Frag mich, was du willst.")

# GPT-Logik
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist eine strategische KI-Zentrale für Barry Gordon, CEO einer Holding."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Fehler bei der GPT-Antwort:\n{str(e)}")
        print("DEBUG – GPT-Fehler:", e)

# App starten
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
