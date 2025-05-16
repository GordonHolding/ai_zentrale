# chainlit.py – inkl. Memory-Verlauf & GPT-only-Logik

import chainlit as cl
import os
import openai

from modules.reasoning_intelligenz.conversation_tracker import (
    log_and_get_context, add_gpt_reply
)
from modules.reasoning_intelligenz.memory_log_search import memory_log_search

openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message
async def main(message):
    user_input = message.content
    user_id = cl.user_session.id
    print(f"🧠 Chainlit Input: {user_input}")

    # 🔎 Memory-Log aktiv durchsuchen (bei Triggerwörtern)
    if any(k in user_input.lower() for k in ["erinnere", "sponsoring", "was war", "bewerbung", "verlauf", "history"]):
        results = memory_log_search(user_input)
        if results:
            summary = "\n".join([
                f"📄 {r.get('summary', r.get('response', '...'))[:150]}" for r in results[:3]
            ])
            await cl.Message(content=summary).send()
            return

    # 🔁 Konversation loggen und an GPT senden
    messages = log_and_get_context(user_id, user_input)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message["content"].strip()
        add_gpt_reply(user_id, reply)

        await cl.Message(content=reply).send()
    except Exception as e:
        await cl.Message(content=f"❌ Systemfehler: {e}").send()
