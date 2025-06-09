# chainlit_app.py – GUI-Fassade der AI-ZENTRALE (Render-kompatibel, onboardingfähig)

import chainlit as cl
from agents.GPTAgent import gpt_agent

@cl.on_chat_start
async def start():
    try:
        # Onboarding aus gpt_agent_onboarding.json laden – über den Kontext des GPTAgent
        onboarding = gpt_agent.get_context_value("onboarding_message")
        # Falls onboarding als Objekt (dict) zurückkommt, nutzen wir den "welcome_message"-Key
        if isinstance(onboarding, dict):
            message = onboarding.get("welcome_message", "Willkommen in der AI-ZENTRALE!")
        elif isinstance(onboarding, str):
            message = onboarding
        else:
            message = "Willkommen in der AI-ZENTRALE!"
    except Exception as e:
        message = f"Willkommen in der AI-ZENTRALE! (Fehler beim Onboarding: {e})"
    
    # Optional: Debug-Log für Render
    print(f"✅ Onboarding geladen: {message}")
    await cl.Message(content=message).send()

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
