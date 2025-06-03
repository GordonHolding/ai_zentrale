# chainlitapp.py – Funktionale Beispiel-Chainlit-App mit Mindestanforderung erfüllt

import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="🧠 Willkommen in der AI-ZENTRALE!").send()

@cl.on_message
async def main(message: cl.Message):
    text = message.content.strip().lower()
    if text in ("hi", "hallo"):
        await cl.Message(content="👋 Hallo! Wie kann ich dir helfen?").send()
    else:
        await cl.Message(content=f"📄 Du hast geschrieben: '{text}'").send()
