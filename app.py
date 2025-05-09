import chainlit as cl

@cl.on_message
async def main(message):
    await cl.Message(content=f"Deine Nachricht war: {message.content}").send()
