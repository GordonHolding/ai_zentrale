# telegram_bot.py

import os
import openai
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from modules.reasoning_intelligenz.conversation_tracker import (
    log_and_get_context, add_gpt_reply
)
from modules.reasoning_intelligenz.memory_log_search import memory_log_search
from modules.input_interfaces.telegram_file_handler import handle_file
from agents.Infrastructure_Agents.TriggerAgent.trigger_router import handle_trigger_input

openai.api_key = os.getenv("OPENAI_API_KEY")

CONFIG_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/"
COMMANDS_PATH = os.path.join(CONFIG_DIR, "telegram_commands.json")
KEYWORDS_PATH = os.path.join(CONFIG_DIR, "gpt_memory_keywords.json")
ACCESS_PATH = os.path.join(CONFIG_DIR, "telegram_access_control.json")

def load_keywords():
    if os.path.exists(KEYWORDS_PATH):
        with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def is_authorized(user_id):
    if not os.path.exists(ACCESS_PATH):
        return True
    with open(ACCESS_PATH, "r", encoding="utf-8") as f:
        allowed = json.load(f).get("allowed_user_ids", [])
        return str(user_id) in allowed

def load_command_list():
    if os.path.exists(COMMANDS_PATH):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as f:
            return [cmd["command"] for cmd in json.load(f)]
    return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen in der AI-Zentrale. Was möchtest du tun?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = str(update.effective_user.id)
    print(f"📩 Telegram Input: {user_input}")

    if not is_authorized(user_id):
        await update.message.reply_text("⛔ Zugriff nicht erlaubt.")
        return

    try:
        # 🔍 Memory-Suche
        if any(k in user_input.lower() for k in load_keywords()):
            results = memory_log_search(user_input)
            if results:
                reply = "\n".join([
                    f"📄 {r.get('summary', r.get('response', '...'))[:150]}" for r in results[:3]
                ])
                await update.message.reply_text(reply)
                return

        # ⚡ Trigger-Kommandos erkennen und auslösen
        if any(cmd in user_input.lower() for cmd in load_command_list()):
            result = handle_trigger_input(user_input)
            await update.message.reply_text(str(result))
            return

        # 🧠 GPT-Verlauf
        messages = log_and_get_context(user_id, user_input)
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message["content"].strip()
        add_gpt_reply(user_id, reply)
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"❌ Fehler: {e}")
        await update.message.reply_text(f"❌ Systemfehler: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
    print("📲 Telegram Bot läuft…")
    app.run_polling()
