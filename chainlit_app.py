# chainlit_app.py – Minimalistische Chainlit-App für AI-ZENTRALE (J.A.R.V.I.S.)

import chainlit as cl
from agents.GPTAgent.gpt_agent import handle_input, startup

# Initialisiere Systemkontext & Begrüßung
system_context = startup()
WELCOME_MSG = system_context.get("welcome_message", "Willkommen! Ich bin J.A.R.V.I.S. – wie kann ich helfen?")
EMOJI_MOOD = system_context.get("emoji_mood", "")
FOOTER_HINT = system_context.get("footer_hint", "")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"{EMOJI_MOOD} {WELCOME_MSG}\n\n{FOOTER_HINT}"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    # User-Input an GPTAgent weiterleiten
    answer = handle_input(message.content)
    final_response = answer.get("final_response") or answer.get("raw_response") or "Fehler: Keine Antwort von J.A.R.V.I.S."
    await cl.Message(content=final_response).send()
