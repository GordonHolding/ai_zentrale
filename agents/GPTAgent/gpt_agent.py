import os
from openai import OpenAI
from utils.json_loader import load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# Initialisiere OpenAI-Client mit API-Key aus Umgebungsvariable (Render-kompatibel)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Lade zentrale GPT-Konfiguration mit Fehlerprüfung
CONFIG = load_json("gpt_config.json")
if not isinstance(CONFIG, dict) or "error" in CONFIG:
    raise RuntimeError(f"Fehler beim Laden der gpt_config.json: {CONFIG.get('error') if isinstance(CONFIG, dict) else 'Unbekannter Fehler'}")

# Setze dynamische Pfade für Prompt + Onboarding aus Konfig, mit robustem Fallback
PROMPT_PATH = CONFIG.get("PROMPT_PATH") or CONFIG.get("gpt_agent_prompt", {}).get("filename") or "gpt_agent_prompt.json"
ONBOARDING_PATH = CONFIG.get("ONBOARDING_PATH") or CONFIG.get("gpt_agent_onboarding", {}).get("filename") or "gpt_agent_onboarding.json"

# Lese Modellparameter aus Konfiguration, robustes Defaulting
MODEL = CONFIG.get("MODEL", {}).get("value") or "gpt-4o"
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value") if isinstance(CONFIG.get("TEMPERATURE", {}), dict) else 0.4
if TEMPERATURE is None:
    TEMPERATURE = 0.4
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value") if isinstance(CONFIG.get("MAX_TOKENS", {}), dict) else 1200
if MAX_TOKENS is None:
    MAX_TOKENS = 1200

# Initialisiere den GPTAgent bei Systemstart
def startup():
    context = initialize_system_context()
    onboarding = load_json(ONBOARDING_PATH)
    if not isinstance(onboarding, dict) or "error" in onboarding:
        raise RuntimeError(f"Fehler beim Laden des Onboarding-Kontexts: {onboarding.get('error') if isinstance(onboarding, dict) else 'Unbekannter Fehler'}")

    # Füge Onboarding-Kontext hinzu (sofort nutzbar für Chainlit etc.)
    context["welcome_message"] = onboarding.get("welcome_message", "Willkommen zurück.")
    context["onboarding_context"] = onboarding
    return context

# Lade Systemprompt aus JSON, robust gegen Fehler
def get_system_prompt():
    prompt_json = load_json(PROMPT_PATH)
    if not isinstance(prompt_json, dict) or "error" in prompt_json:
        raise RuntimeError(f"Fehler beim Laden des Systemprompts: {prompt_json.get('error') if isinstance(prompt_json, dict) else 'Unbekannter Fehler'}")
    return prompt_json.get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")

# Hauptlogik zur Kommunikation mit OpenAI GPT
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
        return {
            "error": f"Fehler bei der GPT-Verarbeitung: {str(e)}"
        }

# Einheitlicher Einstiegspunkt für andere Module / Agenten
def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)
