from main_controller import run_full_system_check

@cl.on_chat_start
async def on_start():
    await cl.Message(content="🧠 Starte Systemcheck...").send()
    result = await run_full_system_check()
    await cl.Message(content=f"✅ Ergebnis:\n{result}").send()
