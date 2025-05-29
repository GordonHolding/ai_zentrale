# drive_router.py – GPT-Anweisungen für DriveAgent analysieren & ausführen

from agents.General_Agents.DriveAgent.drive_agent import DriveAgent
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction

# 📦 Hauptfunktion: verarbeitet GPT-Anweisungen & ruft DriveAgent-Methoden auf
def handle_drive_instruction(instruction: str, metadata: dict = None) -> str:
    agent = DriveAgent()
    metadata = metadata or {}
    instruction_lower = instruction.lower()

    try:
        if any(w in instruction_lower for w in ["verschieben", "move", "verlagere"]):
            file_id = metadata.get("file_id")
            new_parent_id = metadata.get("new_parent_id")
            agent.move(file_id, new_parent_id)
            log_interaction("DriveAgent", f"📂 Datei verschoben", f"{file_id} → {new_parent_id}")
            return "📂 Datei wurde verschoben."

        elif any(w in instruction_lower for w in ["umbenennen", "rename", "neuer name"]):
            file_id = metadata.get("file_id")
            new_name = metadata.get("new_name")
            agent.rename(file_id, new_name)
            log_interaction("DriveAgent", f"📝 Datei umbenannt", f"{file_id} → {new_name}")
            return "📝 Datei wurde umbenannt."

        elif any(w in instruction_lower for w in ["suche", "search", "finden", "finde"]):
            query = metadata.get("query")
            results = agent.search(query)
            log_interaction("DriveAgent", f"🔍 Suche durchgeführt", f"{len(results)} Treffer für: {query}")
            return f"🔍 Es wurden {len(results)} Dateien gefunden."

        elif any(w in instruction_lower for w in ["übersicht", "summary", "inhalt"]):
            folder_id = metadata.get("folder_id")
            summary = agent.summarize(folder_id)
            log_interaction("DriveAgent", f"📦 Ordnerinhalt zusammengefasst", summary)
            return f"📦 Zusammenfassung: {summary}"

        elif any(w in instruction_lower for w in ["metadaten", "details", "info"]):
            file_id = metadata.get("file_id")
            info = agent.metadata(file_id)
            log_interaction("DriveAgent", f"🧾 Metadaten abgerufen", info)
            return f"🧾 Metadaten: {info}"

        elif any(w in instruction_lower for w in ["pdf", "konvertieren", "exportieren"]):
            file_id = metadata.get("file_id")
            result = agent.convert(file_id)
            log_interaction("DriveAgent", f"📤 Datei als PDF exportiert", str(result)[:200])
            return "📤 Datei wurde exportiert."

        elif any(w in instruction_lower for w in ["rechte", "permissions", "zugriff"]):
            file_id = metadata.get("file_id")
            perms = agent.permissions(file_id)
            log_interaction("DriveAgent", f"🔐 Zugriffsrechte abgefragt", perms)
            return f"🔐 Rechte: {perms}"

        return "⚠️ Anweisung nicht erkannt."

    except Exception as e:
        log_interaction("DriveAgent", f"❌ Fehler bei Anweisung: {instruction}", str(e))
        return "❌ Fehler bei der Verarbeitung deiner Anweisung."
