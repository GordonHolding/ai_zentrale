# gpt_agent.py – GPTAgent für AI-ZENTRALE (Render-kompatibel, stabil, clean)

import os
import openai
from utils.json_loader import safe_load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# 🔐 OpenAI API-Key setzen (Render-kompatibel, kein OpenAI() Client)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📦 Konfiguration sicher laden
CONFIG = safe_load_json("gpt_config.json")

# 🗂️ Pfade & Parameter aus Konfiguration mit Fallbacks
PROMPT_PATH = (
    CONFIG.get("PROMPT_PATH")
    or CONFIG.get("gpt_agent_prompt", {}).get("filename")
    or "gpt_agent_prompt.json"
)

MODEL = CONFIG.get("MODEL", {}).get("value", "gpt-4o")
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value", 0.4)
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value", 1200)

# 📄 Prompt-Konfiguration laden
def get_prompt_config():
    return safe_load_json(PROMPT_PATH)

# 🚀 Initialisierung des Agent-Kontextes
def startup():
    context = initialize_system_context()
    prompt_config = get_prompt_config()

    context["welcome_message"] = prompt_config.get("welcome_message", "Willkommen zurück.")
    context["emoji_mood"] = prompt_config.get("emoji_mood", "")
    context["quick_commands"] = prompt_config.get("quick_commands", [])
    context["footer_hint"] = prompt_config.get("footer_hint", "")

    # Optional: weitere Felder für erweitertes UI oder Promptverhalten
    return context

# 📣 Systemprompt abrufen
def get_system_prompt():
    return get_prompt_config().get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")

# 💬 GPT-Abfrage durchführen
def ask_gpt(user_input: str) -> dict:
    try:
        system_prompt = get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        gpt_reply = response.choices[0].message.content.strip()
        parsed = parse_gpt_response(user_input, gpt_reply)
        parsed["final_response"] = gpt_reply
        return parsed

    except Exception as e:
        return {"error": f"Fehler bei der GPT-Verarbeitung: {str(e)}"}

# 🔄 Hauptschnittstelle zur Benutzerinteraktion
def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
