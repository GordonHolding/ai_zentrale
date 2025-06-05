# router_router.py

import openai
from agents.Infrastructure_Agents.RouterAgent.router_prompt_loader import (
    get_system_identity_prompt,
    get_agent_registry_text
)
from agents.Infrastructure_Agents.RouterAgent.router_utils import get_structure_snippet
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

def determine_agent(user_input):
    system_prompt = get_system_identity_prompt()
    agent_registry_text = get_agent_registry_text()
    structure_context = get_structure_snippet()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""
Du erhältst nun eine Benutzeranfrage. Entscheide ausschließlich, **welcher Agent** zuständig ist – basierend auf dem Aufgabenprofil, den verfügbaren Agenten und der Systemstruktur.  
Gib **nur den Agent-Key** zurück (z. B. `drive`, `text`, `memory`).  
Falls kein Agent zuständig ist, gib exakt `none` zurück.

🔹 **User Input:** {user_input}
🔹 **Agentenliste:** {agent_registry_text}
🔹 **Struktureinblick:** {structure_context}
"""}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.1,
            max_tokens=10
        )
        agent_key = response["choices"][0]["message"]["content"].strip().lower()
        log_interaction("RouterRouter", f"Agent gewählt: {agent_key}", user_input)
        return agent_key
    except Exception as e:
        log_interaction("RouterRouter", f"❌ Fehler bei Routing: {e}", user_input)
        return "none"
