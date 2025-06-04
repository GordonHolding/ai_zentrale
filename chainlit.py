import chainlit as cl
import os

if __name__ == "__main__":
    print("🚀 Starte Chainlit App direkt ...")
    cl.run(
        "chainlitapp.py",
        port=int(os.environ.get("CHAINLIT_PORT", 8000)),
        host="0.0.0.0"
    )
