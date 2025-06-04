# router_router.py

import openai
from agents.Infrastructure_Agents.RouterAgent.router_prompt_loader import (
    load_identity_prompt,
    load_dynamic_router_prompt
)
from modules.structure_loader.structure_content_loader import get_structure_snippet  # neue Komponente

def determine_agent(user_input):
    # Struktur-Snippet ergänzen (optional für besseren Kontext)
    structure_context = get_structure_snippet()

    # Prompt zusammenbauen
    prompt = (
        load_identity_prompt()
        + "\n\n"
        + load_dynamic_router_prompt()
        + "\n\n"
        + "📂 Ordnungsübersicht:\n"
        + structure_context
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message["content"].strip()
        return reply
    except Exception as e:
        return f"❌ Routing-Fehler: {e}"
