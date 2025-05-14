# Datei: telegram_bot.py

import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from agents.Infrastructure_Agents.MailAgent.mail_agent import process_emails
from agents.Infrastructure_Agents.MailAgent.mail_agent_prompt import MAIL_AGENT_SYSTEM_PROMPT

openai.api_key = os.getenv("OPENAI_API_KEY")

# Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen in der AI-Zentrale. Wie kann ich Dir helfen?")

# Nachricht verarbeiten & ggf. GPT-Routing starten
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # GPT-Auswertung
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist die KI-Zentrale für Barry Gordon. Analysiere Befehle und leite passende Aktionen ein. Wenn es um E-Mails geht, antworte entsprechend."},
            {"role": "user", "content": user_input}
        ]
    )

    gpt_reply = response.choices[0].message["content"]

    # Erste GPT-Antwort anzeigen
    await update.message.reply_text(f"🤖 GPT: {gpt_reply}")

    # Triggerlogik (vereinfachte Analyse)
    if any(keyword in gpt_reply.lower() for keyword in ["e-mail", "mail", "postfach", "inbox", "scan"]):
        await update.message.reply_text("📬 Starte MailAgent für office@gordonholding.de ...")
        try:
            process_emails("office")
            await update.message.reply_text("✅ MailAgent-Scan abgeschlossen.")
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler beim MailAgent: {e}")

# Bot starten
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("📲 Telegram Bot läuft...")
    app.run_polling()
