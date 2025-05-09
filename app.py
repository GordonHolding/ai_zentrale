import os
import chainlit as cl

@cl.on_message
async def main(message):
    await cl.Message(content=f"Deine Nachricht war: {message.content}").send()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    cl.run(port=port, host="0.0.0.0")
