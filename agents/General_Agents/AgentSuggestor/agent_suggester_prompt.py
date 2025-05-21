# agent_suggester_prompt.py – Promptlogik für strukturabhängige Agentenvorschläge

def generate_agent_suggestion_prompt(structure_blocks, agent_keywords):
    system_msg = {
        "role": "system",
        "content": "Du bist ein intelligenter Vorschlagsagent. Deine Aufgabe ist es, neue oder veränderte Ordnerstrukturen zu erkennen und passende GPT-Agenten vorzuschlagen. Inklusive Name, Aufgabe, Kategorie (General, Infrastructure, Business, Private)."
    }
    user_msg = {
        "role": "user",
        "content": f"Hier ist die aktuelle Struktur: {structure_blocks}\nBekannte Zuordnungen: {agent_keywords}\nBitte identifiziere neue oder unbesetzte Bereiche und schlage passende Agenten vor."
    }
    return [system_msg, user_msg]
