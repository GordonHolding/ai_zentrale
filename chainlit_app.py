# chainlit_app.py – GUI-Fassade der AI-ZENTRALE (vollständig integriert)

import chainlit as cl
from agents.GPTAgent import gpt_agent

# Startet Chainlit mit vollem Systemkontext aus GPTAgent
@cl.on_chat_start
async def start():
    try:
        # Lade Systemkontext inkl. Onboarding
        context = gpt_agent.startup()
        onboarding = context.get("onboarding_context", {})
        message = onboarding.get("welcome_message", "Willkommen zurück.")
    except Exception as e:
        message = f"Willkommen in der AI-ZENTRALE! (Fehler beim Onboarding: {e})"

    print(f"✅ Onboarding geladen: {message}")
    await cl.Message(content=message).send()

# Hauptlogik für Nutzeranfragen
@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.strip()

    if not user_input:
        await cl.Message(content="⚠️ Bitte gib eine gültige Eingabe ein.").send()
        return

    gpt_response = gpt_agent.handle_input(user_input)

    if "error" in gpt_response:
        await cl.Message(content=f"❌ Fehler: {gpt_response['error']}").send()
    else:
        await cl.Message(content=gpt_response["final_response"]).send()
