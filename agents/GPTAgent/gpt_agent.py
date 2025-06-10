# gpt_agent.py

import os
from openai import OpenAI
from utils.json_loader import load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# Hilfsfunktion für robustes JSON-Laden mit Fehlerprüfung
def checked_load_json(filename, context_hint):
    data = load_json(filename)
    if not isinstance(data, dict) or ""error"" in data:
        raise RuntimeError(
            f""Fehler beim Laden von '{context_hint}': {data.get('error') if isinstance(data, dict) else 'Unbekannter Fehler'}""
        )
    return data

# OpenAI-Client initialisieren (Render-kompatibel)
client = OpenAI(api_key=os.getenv(""OPENAI_API_KEY""))

# Zentrale GPT-Konfiguration laden
CONFIG = checked_load_json(""gpt_config.json"", ""gpt_config.json"")

# Dynamische Pfade aus Konfig mit Fallback
PROMPT_PATH = (
    CONFIG.get(""PROMPT_PATH"")
    or CONFIG.get(""gpt_agent_prompt"", {}).get(""filename"")
    or ""gpt_agent_prompt.json""
)
ONBOARDING_PATH = (
    CONFIG.get(""ONBOARDING_PATH"")
    or CONFIG.get(""gpt_agent_onboarding"", {}).get(""filename"")
    or ""gpt_agent_onboarding.json""
)

# Modellparameter aus Konfiguration, robustes Defaulting
MODEL = CONFIG.get(""MODEL"", {}).get(""value"") or ""gpt-4o""
TEMPERATURE = CONFIG.get(""TEMPERATURE"", {}).get(""value"") if isinstance(CONFIG.get(""TEMPERATURE"", {}), dict) else 0.4
if TEMPERATURE is None:
    TEMPERATURE = 0.4
MAX_TOKENS = CONFIG.get(""MAX_TOKENS"", {}).get(""value"") if isinstance(CONFIG.get(""MAX_TOKENS"", {}), dict) else 1200
if MAX_TOKENS is None:
    MAX_TOKENS = 1200

def startup():
    context = initialize_system_context()
    onboarding = checked_load_json(ONBOARDING_PATH, ONBOARDING_PATH)
    context[""welcome_message""] = onboarding.get(""welcome_message"", ""Willkommen zurück."")
    context[""onboarding_context""] = onboarding
    return context

def get_system_prompt():
    prompt_json = checked_load_json(PROMPT_PATH, PROMPT_PATH)
    return prompt_json.get(""system_prompt"", ""Du bist ein hilfsbereiter KI-Agent."")

def ask_gpt(user_input: str) -> dict:
    try:
        system_prompt = get_system_prompt()
        messages = [
            {""role"": ""system"", ""content"": system_prompt},
            {""role"": ""user"", ""content"": user_input}
        ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        gpt_reply = response.choices[0].message.content.strip()
        parsed = parse_gpt_response(user_input, gpt_reply)
        parsed[""final_response""] = gpt_reply
        return parsed

    except Exception as e:
        return {
            ""error"": f""Fehler bei der GPT-Verarbeitung: {str(e)}""
        }

def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
