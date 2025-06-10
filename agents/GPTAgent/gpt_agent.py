# agents.GPTAgent.gpt_agent.py

from openai import OpenAI
from utils.json_loader import load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context
from agents.GPTAgent.gpt_response_parser import parse_gpt_response
import os

# OpenAI-Client (Render-kompatibel)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT-Konfiguration laden
CONFIG = load_json("gpt_config.json")
PROMPT_FILE = CONFIG.get("gpt_agent_prompt", {}).get("filename", "gpt_agent_prompt.json")
ONBOARDING_FILE = CONFIG.get("gpt_agent_onboarding", {}).get("filename", "gpt_agent_onboarding.json")
MODEL = CONFIG.get("MODEL", {}).get("value", "gpt-4o")
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value", 0.4)
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value", 1200)

# Prompt & Onboarding laden
def get_system_prompt():
    return load_json(PROMPT_FILE).get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")

def get_onboarding():
    return load_json(ONBOARDING_FILE)

# Initialisiert den GPTAgent bei Systemstart
def startup():
    context = initialize_system_context()
    context.update(get_onboarding())  # z. B. welcome_message etc.
    return context

# Hauptkommunikation mit GPT
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
        return {"error": f"Fehler bei der GPT-Verarbeitung: {str(e)}"}

def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
