# chainlit.py – mit Datei-Upload, Verlauf und GPT-Verknüpfung

import chainlit as cl
import os
import openai
from tempfile import NamedTemporaryFile

from modules.reasoning_intelligenz.conversation_tracker import log_and_get_context, add_gpt_reply, attach_file_summary
from modules.output_infrastruktur.file_uploader import save_uploaded_file

openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message
async def main(message):
    user_input = message.content
    user_id = cl.user_session.id

    print(f"🧠 Chainlit Input von {user_id}: {user_input}")

    # Verlauf laden + neue Eingabe loggen
    messages = log_and_get_context(user_id, user_input)

    # GPT-Call mit vollem Verlauf
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    reply = response.choices[0].message.content
    add_gpt_reply(user_id, reply)

    await cl.Message(content=reply).send()


@cl.on_file_upload
async def handle_upload(file):
    user_id = cl.user_session.id
    tmp_path = None

    # Temporäre Datei schreiben
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.content.read())
        tmp_path = tmp.name

    # Datei speichern + Memory verknüpfen
    save_uploaded_file(
        user_id=user_id,
        file_path=tmp_path,
        original_filename=file.name,
        description="Upload via Chainlit-Interface"
    )

    # GPT erhält Info
    attach_file_summary(user_id, f"Datei: {file.name}")

    await cl.Message(content=f"📎 Datei empfangen: {file.name}").send()

    # Optional: automatische Nachverarbeitung anstoßen (später z. B. GPT-Vision, PDF-Summary)


@cl.on_chat_start
async def greet():
    await cl.Message(content="Willkommen in der AI-Zentrale. Was möchtest du tun?").send()
