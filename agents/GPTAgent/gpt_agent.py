# agents.GPTAgent.gpt_agent.py

from openai import OpenAI
from utils.json_loader import load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response
import os

# OpenAI-Client mit API-Key aus Umgebungsvariable (Render-kompatibel)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Lade GPT-Konfigurationen aus JSON
CONFIG = load_json("gpt_config.json")
PROMPT_PATH = CONFIG.get("PROMPT_PATH", "gpt_agent_prompt.json")
MODEL = CONFIG.get("MODEL", "gpt-4o")
TEMPERATURE = CONFIG.get("TEMPERATURE", 0.4)
MAX_TOKENS = CONFIG.get("MAX_TOKENS", 1200)

# Initialisiert den GPTAgent bei Systemstart
def startup():
    context = initialize_system_context()
    return context

# Holt den aktiven GPT-Systemprompt (als Grundlage für GPT)
def get_system_prompt():
    return load_json(PROMPT_PATH).get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")

# Führt die Hauptkommunikation mit OpenAI GPT durch
def ask_gpt(user_input: str) -> dict:
    system_prompt = get_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
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
        return {
            "error": f"Fehler bei der GPT-Verarbeitung: {str(e)}"
        }

# Zentrale Eingabeverarbeitung (kann von anderen Agents genutzt werden)
def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
