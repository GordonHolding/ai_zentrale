# drive_triggers.py
# 🧠 Lokale Triggerlogik für den DriveAgent – z. B. bei Scan, Neustart, Dateiupdate

from agents.General_Agents.DriveAgent.drive_agent import DriveAgent
from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from agents.General_Agents.DriveAgent.drive_config import ROOT_FOLDER_ID


# ⚡ Trigger bei Systemstart (z. B. für Initialscan oder Index)
def trigger_on_startup():
    agent = DriveAgent()
    summary = agent.summarize(ROOT_FOLDER_ID)
    log_interaction("DriveAgent", "🔁 Trigger on Startup ausgeführt", summary)
    return summary

# ⚡ Trigger bei neuem Datei-Upload oder externem Ereignis
def trigger_on_new_file(file_id):
    agent = DriveAgent()
    metadata = agent.metadata(file_id)
    log_interaction("DriveAgent", f"📎 Neuer Upload erkannt: {metadata['name']}", metadata)
    return metadata

# ⚡ Trigger bei externer GPT-Anfrage zur Suche
def trigger_on_search_request(search_query):
    agent = DriveAgent()
    results = agent.search(search_query)
    log_interaction("DriveAgent", f"🔍 Suche ausgelöst: {search_query}", f"{len(results)} Treffer")
    return
