# chainlit.py – Minimal + Backend-Controller

import chainlit as cl
import subprocess

# ▶ Starte Backend-Controller (async, blockiert Chainlit nicht)
subprocess.Popen(["python3", "main_controller.py"])

# ✅ Reagiere auf Eingaben
@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content="✅ Chainlit läuft & MainController wurde gestartet!").send()
