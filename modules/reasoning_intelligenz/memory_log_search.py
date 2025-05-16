import json
import os
from typing import List, Dict

MEMORY_LOG_PATH = "memory_log.json"

def memory_log_search(criteria: str) -> List[Dict]:
    """
    Durchsucht das Memory-Log nach Keywords im Kontext von GPT-Antworten, E-Mails oder Notizen.
    """
    if not os.path.exists(MEMORY_LOG_PATH):
        return [{"result": "🔍 Kein Memory-Log vorhanden."}]

    with open(MEMORY_LOG_PATH) as f:
        try:
            memory = json.load(f)
        except json.JSONDecodeError:
            return [{"result": "⚠️ Fehler beim Lesen der Memory-Logdatei."}]

    # Filterfunktion: einfache Teiltextsuche über Schlüsselwerte
    matches = []
    for entry in memory:
        entry_text = " ".join([
            str(entry.get("prompt", "")),
            str(entry.get("response", "")),
            str(entry.get("summary", "")),
            str(entry.get("subject", "")),
            str(entry.get("category", "")),
            str(entry.get("type", ""))
        ]).lower()

        if criteria.lower() in entry_text:
            matches.append(entry)

    if not matches:
        return [{"result": f"❌ Keine Einträge gefunden für: '{criteria}'"}]

    return matches
