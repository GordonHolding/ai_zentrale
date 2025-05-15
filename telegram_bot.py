# Datei: telegram_bot.py

import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from agents.Infrastructure_Agents.RouterAgent.router_agent import handle_user_input
from modules.reasoning_intelligenz.global_identity_prompt import load_global_identity_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

# Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen in der AI-Zentrale. Was möchtest du tun?")

# Nachricht verarbeiten & an RouterAgent weitergeben
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(f"📩 Telegram Input: {user_input}")

    try:
        system_prompt = load_global_identity_prompt()

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message["content"].strip()
        print(f"🤖 RouterAgent-Antwort: {reply}")
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"❌ Fehler: {e}")
        await update.message.reply_text(f"❌ Systemfehler: {e}")

# Telegram-Bot starten
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("📲 Telegram Bot läuft...")
    app.run_polling()
