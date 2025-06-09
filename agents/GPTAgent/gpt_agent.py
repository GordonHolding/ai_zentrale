# agents.GPTAgent.gpt_agent.py

from openai import ChatCompletion
from utils.json_loader import load_json
from agents.GPTAgent.startup_loader import initialize_system_context
from agents.Infrastructure_Agents.GPTAgent.context_manager import refresh_context, get_context_value
from agents.Infrastructure_Agents.GPTAgent.gpt_response_parser import parse_gpt_response

# 🔗 Lade Konfiguration aus zentralem JSON
CONFIG = load_json(""GPTAgent/GPTAgent_Protokolle/gpt_config.json"")
PROMPT_PATH = CONFIG.get(""PROMPT_PATH"", ""GPTAgent/GPTAgent_Kontexte_Promptweitergaben/gpt_agent_prompt.json"")
MODEL = CONFIG.get(""MODEL"", ""gpt-4o"")
TEMPERATURE = CONFIG.get(""TEMPERATURE"", 0.4)
MAX_TOKENS = CONFIG.get(""MAX_TOKENS"", 1200)

# 🚀 Systeminitialisierung (z. B. bei Start durch startup_triggers oder chainlit)
def startup():
    return initialize_system_context()

# 🧠 Lade dynamisch den aktiven Systemprompt
def get_system_prompt() -> str:
    prompt_data = load_json(PROMPT_PATH)
    return prompt_data.get(""system_prompt"", ""Du bist ein hilfsbereiter KI-Agent."")

# 💬 GPT-Kommunikation: schickt Anfrage an OpenAI GPT
def ask_gpt(user_input: str) -> dict:
    system_prompt = get_system_prompt()
    messages = [
        {""role"": ""system"", ""content"": system_prompt},
        {""role"": ""user"", ""content"": user_input}
    ]

    try:
        response = ChatCompletion.create(
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

# 🧩 High-Level-Handling – inkl. Kontexterfrischung
def handle_input(user_input: str) -> dict:
    refresh_context()
    return ask_gpt(user_input)"
