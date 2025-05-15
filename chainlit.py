# Datei: chainlit.py

import os
import chainlit as cl
import openai

from agents.Infrastructure_Agents.RouterAgent.router_agent import handle_user_input
from modules.reasoning_intelligenz.global_identity_prompt import load_global_identity_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message
async def main(message):
    user_input = message.content
    print(f"🧠 Chainlit Input: {user_input}")

    # Lade Identitätslayer (Systemverständnis)
    identity_prompt = load_global_identity_prompt()

    # Übergabe an RouterAgent inkl. Identität
    result = handle_user_input(user_input, identity_prompt=identity_prompt)

    # Antwort an User zurücksenden
    await cl.Message(content=str(result)).send()
