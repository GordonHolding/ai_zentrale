# chainlit_app.py – Minimalistische Chainlit-App für AI-ZENTRALE (J.A.R.V.I.S.)

import chainlit as cl
from agents.GPTAgent.gpt_agent import handle_input, startup

# Systemkontext initialisieren und Begrüßung holen
system_context = startup()
WELCOME_MSG = system_context.get("welcome_message", "Willkommen!")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content=WELCOME_MSG).send()

@cl.on_message
async def on_message(message: cl.Message):
    answer = handle_input(message.content)
    # GPT denkt & spricht immer im system_prompt-Stil (siehe gpt_agent.py)
    final_response = answer.get("final_response") or "Fehler: Keine Antwort."
    await cl.Message(content=final_response).send()
