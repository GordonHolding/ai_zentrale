# chainlit_app.py – GUI-Fassade der AI-ZENTRALE (inkl. Debug-Ausgabe des Prompts)

import chainlit as cl
from agents.GPTAgent import gpt_agent

# Starte Chat mit geladenem Onboarding + sichtbarem Systemprompt (Debug)
@cl.on_chat_start
async def start():
    try:
        # Starte Systemkontext inkl. Onboarding
        context = gpt_agent.startup()
        onboarding = context.get("onboarding_context", {})
        message = onboarding.get("welcome_message", "Willkommen zurück.")
    except Exception as e:
        message = f"Willkommen in der AI-ZENTRALE! (Fehler beim Onboarding: {e})"

    # Begrüßung anzeigen
    await cl.Message(content=message).send()

    # Debug: Aktueller Prompt anzeigen
    try:
        system_prompt = gpt_agent.get_system_prompt()
        await cl.Message(content=f"🧪 Debug Prompt:\n{system_prompt}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Fehler beim Laden des Prompts: {e}").send()

# Hauptverarbeitung jeder Nutzernachricht
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
