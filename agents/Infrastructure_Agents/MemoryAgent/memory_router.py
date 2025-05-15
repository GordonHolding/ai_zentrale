# memory_router.py

import openai
from memory_config import MEMORY_LOG_PATH

def gpt_route_memory_action(entry_summary):
    """
    Fragt GPT, was mit einem bestimmten Memory-Eintrag geschehen soll
    (Antwort senden, Ablegen, Weiterleiten etc.)
    """
    prompt = f"""
Du bist der Memory-Router der Gordon Holding. 
Ein neuer Memory-Eintrag wurde gespeichert:

"{entry_summary}"

Was soll mit diesem Eintrag geschehen? Gib mir nur eine klare Anweisung: 
z. B. "weiterleiten an InvestorAgent", "antworten", "archivieren", "ignorieren".
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein Routing-Assistent für Memory-Einträge."},
                {"role": "user", "content": prompt}
            ]
        )
        decision = response.choices[0].message["content"].strip()
        print(f"[GPT-Router] Entscheidung: {decision}")
        return decision
    except Exception as e:
        print(f"❌ GPT-Routing-Fehler: {e}")
        return "unentschieden"
