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
