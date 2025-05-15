# router_router.py

import openai

def determine_agent(user_input):
    """
    GPT entscheidet, welcher Spezialagent zuständig ist.
    """

    prompt = f"""
Du bist der zentrale RouterAgent der Gordon Holding.
Analysiere den folgenden Nutzereingabetext und bestimme, welcher Spezialagent zuständig ist:

"{user_input}"

Antwortoptionen:
- "mail" → für E-Mail-Themen
- "memory" → für Gedächtnis, Protokolle, Entscheidungen
- "unbekannt" → wenn nicht klar
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein Routing-Agent für AI-Agentenarchitekturen."},
                {"role": "user", "content": prompt}
            ]
        )
        decision = response.choices[0].message["content"].strip().lower()
        print(f"🔀 GPT Routing: {decision}")
        return decision

    except Exception as e:
        print(f"❌ Routing-Fehler: {e}")
        return "unbekannt"
