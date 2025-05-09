import chainlit as cl

@cl.on_message
async def main(message):
    await cl.Message(content=f"Deine Nachricht war: {message.content}").send()

if __name__ == "__main__":
    cl.run(port=10000, host="0.0.0.0")
