# Datei: chainlit.py

import chainlit as cl
import os
import openai

from agents.Infrastructure_Agents.RouterAgent.router_agent import handle_user_input

openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message
async def main(message):
    user_input = message.content
    print(f"🧠 Chainlit Input: {user_input}")

    # Übergabe an RouterAgent zur Analyse & Entscheidung
    result = handle_user_input(user_input)

    # Antwort an User zurücksenden
    await cl.Message(content=str(result)).send()
