# Datei: chainlit.py
import chainlit as cl
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message
async def main(message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist die visuelle AI-Zentrale für Barry Gordon. Antworte kurz, smart und CI-konform."},
            {"role": "user", "content": message.content}
        ]
    )
    await cl.Message(content=response.choices[0].message.content).send()
