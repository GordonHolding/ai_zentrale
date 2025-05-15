# interface_router.py

import openai

def determine_agent(user_input):
    """
    GPT entscheidet anhand des Inputs, welcher Agent zuständig ist.
    """

    prompt = f"""
Du bist der InterfaceAgent der Gordon Holding. Analysiere den folgenden Nutzerbefehl und bestimme den zuständigen Spezialagenten:

"{user_input}"

Antwortoptionen:
- "mail" → für E-Mail-Verwaltung, Posteingang, Label, Antworten
- "memory" → für Fragen zu früheren Entscheidungen, Zusammenfassungen, GPT-Protokolle
- "unbekannt" → wenn unklar
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein Routing-System für Spezialagenten."},
                {"role": "user", "content": prompt}
            ]
        )
        decision = response.choices[0].message["content"].strip().lower()
        print(f"🔀 GPT hat entschieden: {decision}")
        return decision
    except Exception as e:
        print(f"❌ Fehler beim Agent-Routing: {e}")
        return "unbekannt"
