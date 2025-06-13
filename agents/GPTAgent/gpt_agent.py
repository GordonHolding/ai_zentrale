# gpt_agent.py – GPTAgent für AI-ZENTRALE (sicher & strukturiert)

import os
from openai import OpenAI
from utils.json_loader import load_json_from_gdrive
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# 🧠 API-Key laden und prüfen (Deployment-sicher)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY nicht gesetzt – GPTAgent kann nicht starten.")
client = OpenAI(api_key=api_key)

# 🗂️ GPT-Konfiguration laden (direkt)
CONFIG = load_json_from_gdrive("gpt_config.json")

# 📁 Dynamische Pfade aus Konfiguration oder Defaults
PROMPT_PATH = (
    CONFIG.get("PROMPT_PATH")
    or CONFIG.get("gpt_agent_prompt", {}).get("filename")
    or "gpt_agent_prompt.json"
)

# ⚙️ Modellparameter mit Fallback
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value", 0.4)
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value", 1200)
MODEL = CONFIG.get("MODEL", {}).get("value", "gpt-4o")

# 📥 Prompt-Konfiguration laden
def get_prompt_config():
    return load_json_from_gdrive(PROMPT_PATH)

# 🚀 Initialisierung des Systemkontextes
def startup():
    context = initialize_system_context()
    prompt_config = get_prompt_config()
    context["welcome_message"] = prompt_config.get("welcome_message", "Willkommen zurück.")
    context["emoji_mood"] = prompt_config.get("emoji_mood", "")
    context["quick_commands"] = prompt_config.get("quick_commands", [])
    context["footer_hint"] = prompt_config.get("footer_hint", "")
    return context

# 🧾 Systemprompt abrufen
def get_system_prompt():
    return get_prompt_config().get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")

# 💬 GPT-Antwort generieren
def ask_gpt(user_input: str) -> dict:
    try:
        system_prompt = get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        response = client.chat.completions.create(
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

# 🎛️ Hauptfunktion zur Eingabeverarbeitung
def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
