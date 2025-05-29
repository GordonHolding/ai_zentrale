# memory_selector.py – Bewertungslogik für GPT-Langzeitspeicher

from datetime import datetime
from typing import List, Dict

# 🧠 Bewertet, ob ein Inhalt speicherwürdig ist
def is_valuable(content: str) -> bool:
    keywords = ["Geburtstag", "Firma", "Systemregel", "Rolle", "IP", "Konzept", "Investor", "Reminder"]
    return any(keyword.lower() in content.lower() for keyword in keywords) or len(content) > 300

# 🏷️ Extrahiert potenzielle Tags aus Inhalt
def extract_tags(content: str) -> List[str]:
    tags = []
    if "finanz" in content.lower():
        tags.append("Finanzen")
    if "investor" in content.lower():
        tags.append("Investor")
    if "familie" in content.lower():
        tags.append("Privat")
    if "gpt" in content.lower():
        tags.append("System")
    return tags if tags else ["Sonstiges"]

# 🧾 Erstellt kompakte Zusammenfassung
def suggest_memory_summary(content: str) -> str:
    snippet = content.strip().replace("\n", " ")
    return snippet[:160] + ("..." if len(snippet) > 160 else "")

# 📁 Erstellt vollständigen Memory-Eintrag
def build_memory_entry(user_id: str, content: str) -> Dict:
    return {
        "user": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "content": content,
        "summary": suggest_memory_summary(content),
        "tags": extract_tags(content),
        "source": "memory_selector",
        "category": "GPT"
    }

# ✅ NEU: Zusammenfassung aus aktuellem Kontext (für context_triggers)
def extract_summary_from_context(context_block: List[List[Dict]]) -> str:
    if not context_block or not context_block[-1]:
        return "Kein Kontext vorhanden."
    last_messages = context_block[-1][-4:]
    return " / ".join(entry["content"][:60] for entry in last_messages)

# ✅ NEU: Zusammenfassung aus Langzeitverlauf (für conversation_triggers)
def extract_summary_from_conversation(history_block: List[Dict]) -> str:
    if not history_block:
        return "Kein Verlauf vorhanden."
    last_entries = history_block[-4:]
    return " / ".join(entry["content"][:60] for entry in last_entries)
