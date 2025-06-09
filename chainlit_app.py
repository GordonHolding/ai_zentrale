# chainlit_app.py – GUI-Fassade der AI-ZENTRALE

import chainlit as cl
from agents.Infrastructure_Agents.GPTAgent import gpt_agent

@cl.on_chat_start
async def start():
    # Lade dynamisch das Onboarding aus gpt_agent_onboarding.json
    onboarding = gpt_agent.get_context_value(""onboarding_message"")  # <- kommt aus context_manager
    await cl.Message(content=onboarding or ""🧠 Willkommen in der AI-ZENTRALE!"").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.strip()

    if not user_input:
        await cl.Message(content=""⚠️ Bitte gib eine gültige Eingabe ein."").send()
        return

    gpt_response = gpt_agent.handle_input(user_input)

    if ""error"" in gpt_response:
        await cl.Message(content=f""❌ Fehler: {gpt_response['error']}"").send()
    else:
        await cl.Message(content=gpt_response[""final_response""]).send()
