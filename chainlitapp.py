# chainlitapp.py – Minimale Beispiel-Chainlit-App

import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.strip()
    if user_input.lower() in ("hallo", "hi"):
        await cl.Message(content="👋 Hallo! Wie kann ich dir helfen?").send()
    else:
        await cl.Message(content=f"Du hast geschrieben: '{user_input}'").send()
