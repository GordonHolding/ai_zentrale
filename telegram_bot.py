import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# API-Keys laden
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_KEY")

# Begrüßung bei /start
def start(update, context):
    update.message.reply_text("Hi Barry, ich bin dein Telegram-GPT. Frag mich, was du willst.")

# GPT-Antwortlogik mit Fehlerausgabe
def handle_message(update, context):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist eine strategische KI für Barry Gordon, CEO einer Holding."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Fehler bei der GPT-Antwort:\n{str(e)}"
    update.message.reply_text(reply)

# Main-Funktion
def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
