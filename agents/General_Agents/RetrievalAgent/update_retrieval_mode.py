# update_retrieval_mode.py – Umschalten zwischen OpenAI / Local

from utils.json_loader import load_json, write_json

def set_retrieval_mode(mode: str) -> str:
    mode = mode.lower()
    if mode not in ["local", "openai"]:
        return f"❌ Ungültiger Modus: {mode}"

    config = load_json("retrieval_config.json")
    config["mode"] = mode
    write_json("retrieval_config.json", config)
    return f"✅ retrieval_config.json erfolgreich gesetzt auf: {mode}"
