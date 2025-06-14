# gpt_agent.py – GPTAgent für AI-ZENTRALE (sicher, robust & debug-freundlich)

import os
import traceback
from openai import OpenAI
from utils.json_loader import load_json_from_gdrive
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.GPTAgent.gpt_response_parser import parse_gpt_response

# Debug-Logging (optional in Datei)
# LOGFILE = "/tmp/gpt_agent_debug.log"
def dbg(msg):
    print(msg)
    # Mit Logdatei:
    # with open(LOGFILE, "a") as f:
    #     f.write(str(msg) + "\n")

# 🧠 API-Key laden und prüfen (Deployment-sicher)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    dbg("[GPTAgent][ERROR] OPENAI_API_KEY nicht gesetzt!")
    raise EnvironmentError("OPENAI_API_KEY nicht gesetzt – GPTAgent kann nicht starten.")
client = OpenAI(api_key=api_key)
dbg("[GPTAgent] OpenAI-Client initialisiert.")

# 🗂️ GPT-Konfiguration laden (direkt)
CONFIG = load_json_from_gdrive("gpt_config.json")
dbg(f"[GPTAgent] GPT-Konfiguration geladen: {CONFIG}")

# 📁 Dynamische Pfade aus Konfiguration oder Defaults
PROMPT_PATH = (
    CONFIG.get("PROMPT_PATH")
    or CONFIG.get("gpt_agent_prompt", {}).get("filename")
    or "gpt_agent_prompt.json"
)
dbg(f"[GPTAgent] Verwende Prompt-Pfad: {PROMPT_PATH}")

# ⚙️ Modellparameter mit Fallback
TEMPERATURE = CONFIG.get("TEMPERATURE", {}).get("value", 0.4)
MAX_TOKENS = CONFIG.get("MAX_TOKENS", {}).get("value", 1200)
MODEL = CONFIG.get("MODEL", {}).get("value", "gpt-4o")
dbg(f"[GPTAgent] Model: {MODEL} | Temp: {TEMPERATURE} | MaxTokens: {MAX_TOKENS}")

# 📥 Prompt-Konfiguration laden
def get_prompt_config():
    config = load_json_from_gdrive(PROMPT_PATH)
    dbg(f"[GPTAgent] Prompt-Konfiguration geladen: {config}")
    return config

# 🚀 Initialisierung des Systemkontextes
def startup():
    context = initialize_system_context()
    prompt_config = get_prompt_config()
    context["welcome_message"] = prompt_config.get("welcome_message", "Willkommen zurück.")
    context["emoji_mood"] = prompt_config.get("emoji_mood", "")
    context["quick_commands"] = prompt_config.get("quick_commands", [])
    context["footer_hint"] = prompt_config.get("footer_hint", "")
    dbg(f"[GPTAgent] Systemkontext initialisiert: {context}")
    return context

# 🧾 Systemprompt abrufen
def get_system_prompt():
    prompt_conf = get_prompt_config()
    sp = prompt_conf.get("system_prompt", "Du bist ein hilfsbereiter KI-Agent.")
    dbg(f"[GPTAgent] Systemprompt geladen: {sp[:100]}...")
    return sp

# 💬 GPT-Antwort generieren
def ask_gpt(user_input: str) -> dict:
    try:
        system_prompt = get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        dbg(f"[GPTAgent][Request] Sende an OpenAI: Model={MODEL}, Prompt={system_prompt[:80]}..., UserInput={user_input}")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        dbg(f"[GPTAgent][Response] OpenAI Antwort erhalten: {response}")
        if not hasattr(response, "choices") or not response.choices:
            dbg("[GPTAgent][ERROR] OpenAI-Antwort leer – keine choices erhalten.")
            return {"error": "OpenAI-Antwort leer – keine choices erhalten."}
        gpt_reply = response.choices[0].message.content.strip()
        if not gpt_reply:
            dbg("[GPTAgent][ERROR] OpenAI-Antwort leer – kein Content erhalten.")
            return {"error": "OpenAI-Antwort leer – kein Content erhalten."}
        parsed = parse_gpt_response(user_input, gpt_reply)
        parsed["final_response"] = gpt_reply
        dbg(f"[GPTAgent][Parsed] {parsed}")
        return parsed
    except Exception as e:
        tb = traceback.format_exc()
        dbg(f"[GPTAgent][EXCEPTION] {e}\n{tb}")
        return {"error": f"Fehler bei der GPT-Verarbeitung: {str(e)}"}

# 🎛️ Hauptfunktion zur Eingabeverarbeitung
def handle_input(user_input: str) -> dict:
    refresh_context()
    dbg(f"[GPTAgent] handle_input() aufgerufen mit user_input: {user_input}")
    return ask_gpt(user_input)
