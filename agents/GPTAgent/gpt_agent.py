# gpt_agent.py – GPTAgent für AI-ZENTRALE (sicher & strukturiert)

import os
from openai import OpenAI
from utils.json_loader import checked_load_json, safe_load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# 🧠 OpenAI-Client initialisieren (Render-kompatibel)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🗂️ GPT-Konfiguration laden (robust)
CONFIG = safe_load_json("gpt_config.json")
if "error" in CONFIG:
    print(f"⚠️ Fehler beim Laden der GPT-Konfiguration: {CONFIG['error']}")
    CONFIG = {}

# 📁 Dynamische Pfade aus Konfiguration oder Defaults
PROMPT_PATH = (
    CONFIG.get("PROMPT_PATH")
    or CONFIG.get("gpt_agent_prompt", {}).get("filename")
    or "gpt_agent_prompt.json"
)

# ⚙️ Modellparameter mit Fallback
MODEL = CONFIG.get("MODEL", {}).get("value") or "gpt-4o"
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value") if isinstance(CONFIG.get("TEMPERATURE", {}), dict) else 0.4
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value") if isinstance(CONFIG.get("MAX_TOKENS", {}), dict) else 1200
if TEMPERATURE is None:
    TEMPERATURE = 0.4
if MAX_TOKENS is None:
    MAX_TOKENS = 1200

# 📥 Prompt-Konfiguration laden (robust)
def get_prompt_config():
    prompt_config = safe_load_json(PROMPT_PATH)
    if "error" in prompt_config:
        print(f"⚠️ Fehler beim Laden des Systemprompts: {prompt_config['error']}")
        return {}
    return prompt_config

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
