# conversation_triggers.py – Langzeitgedächtnis-Steuerung (Persistent Memory)

from agents.Infrastructure_Agents.MemoryAgent import conversation_tracker
from agents.Infrastructure_Agents.MemoryAgent.memory_selector import extract_summary_from_conversation
import datetime

# 🧠 Langzeit-Snapshot bei strategisch relevanten Inhalten
def save_longterm_memory(user_id: str):
    history = conversation_tracker.get_conversation(user_id)
    if not history:
        return "Kein Gesprächsverlauf zum Speichern gefunden."
    summary = extract_summary_from_conversation(history)
    conversation_tracker.log_system_note(user_id, f"📥 Wichtiges langfristig gespeichert: {summary}")
    return "Gesprächsverlauf wurde als langfristige Erinnerung gespeichert."

# ❌ Langzeitgedächtnis löschen (z. B. bei „vergiss meine Daten“)
def forget_longterm_memory(user_id: str):
    conversation_tracker.reset_conversation(user_id)
    return "Langzeitgedächtnis wurde gelöscht."

# 🔁 Langzeitkontext abrufen (z. B. bei „was weißt du noch über...“)
def recall_longterm_memory(user_id: str):
    history = conversation_tracker.get_conversation(user_id)
    if not history:
        return "Keine gespeicherte Langzeit-Konversation vorhanden."
    return history

# 🧾 Langzeitspeicher anzeigen (Ausgabeformat für Debug/Review)
def show_longterm_summary(user_id: str):
    history = conversation_tracker.get_conversation(user_id)
    if not history:
        return "Langzeitspeicher ist leer."
    formatted = "\n".join([f"{entry['role']}: {entry['content']}" for entry in history[-6:]])
    return f"Letzte gespeicherte Einträge:\n\n{formatted}"
