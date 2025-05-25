# chainlit.py – Eingangs-Interface für AI-ZENTRALE

import chainlit as cl
import os
import openai
import json

from modules.reasoning_intelligenz.conversation_tracker import (
    log_and_get_context, add_gpt_reply
)
from agents.Infrastructure_Agents.MemoryAgent.memory_log_search import memory_log_search
from agents.Infrastructure_Agents.TriggerAgent.trigger_router import handle_trigger_input

openai.api_key = os.getenv("OPENAI_API_KEY")

CONFIG_DIR = "0.3 AI-Regelwerk & Historie/Systemregeln/Config/"
KEYWORDS_PATH = os.path.join(CONFIG_DIR, "gpt_memory_keywords.json")

def load_keywords():
    if os.path.exists(KEYWORDS_PATH):
        with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@cl.on_message
async def on_message(message):
    user_input = message.content
    user_id = cl.user_session.id
    print(f"🧠 Chainlit Input: {user_input}")

    try:
        # 🔍 Memory Trigger
        if any(k in user_input.lower() for k in load_keywords()):
            results = memory_log_search(user_input)
            if results:
                summary = "\n".join([
                    f"📄 {r.get('summary', r.get('response', '...'))[:150]}" for r in results[:3]
                ])
                await cl.Message(content=summary).send()
                return

        # ⚡ Trigger Dispatch (derzeit optional, wird später scharfgestellt)
        if any(trigger_word in user_input.lower() for trigger_word in ["systemscan", "guardian", "zeittrigger", "reminder"]):
            result = handle_trigger_input(user_input)
            await cl.Message(content=str(result)).send()
            return

        # 🧠 GPT-Antwort mit Kontext
        messages = log_and_get_context(user_id, user_input)
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message["content"].strip()
        add_gpt_reply(user_id, reply)
        await cl.Message(content=reply).send()

    except Exception as e:
        await cl.Message(content=f"❌ Systemfehler: {str(e)}").send()
