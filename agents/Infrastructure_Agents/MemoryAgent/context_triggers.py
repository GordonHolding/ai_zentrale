# context_triggers.py – Kurzzeit-Gedächtnissteuerung (Session-Kontext)

import datetime
from agents.Infrastructure_Agents.MemoryAgent import context_tracker
from agents.Infrastructure_Agents.MemoryAgent.memory_selector import extract_summary_from_context

# 🧠 Kontext-Snapshot für neue Session
def mark_session_start(user_id: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    context_tracker.attach_file_summary(user_id, f"🆕 Neue Session gestartet: {timestamp}")

# 💬 Kontext speichern nach manuellem Befehl („merk dir das“, „speichere das“ etc.)
def save_current_context(user_id: str):
    current = context_tracker.get_context(user_id)
    if not current:
        return "Kein aktueller Kontext zum Speichern vorhanden."
    summary = extract_summary_from_context(current)
    context_tracker.attach_file_summary(user_id, f"📌 Kontext gespeichert: {summary}")
    return "Der aktuelle Kontext wurde gespeichert."

# ❌ Kontext vergessen („vergiss das“, „lösche den Verlauf“ etc.)
def forget_context(user_id: str):
    context_tracker.reset_context(user_id)
    return "Der aktive Gesprächskontext wurde gelöscht."

# 🔄 Kontext rekonstruieren (z. B. bei „erinnere dich an...“)
def recall_last_context(user_id: str):
    context = context_tracker.get_context(user_id)
    if not context:
        return "Kein vorheriger Kontext gefunden."
    return context

# 🧾 Kontext anzeigen (optional via Chat-Kommando: „was weißt du noch?“)
def show_current_context(user_id: str):
    context = context_tracker.get_context(user_id)
    if not context:
        return "Ich habe aktuell keinen Kontext gespeichert."
    formatted = "\n".join([f"{c['role']}: {c['content']}" for c in context[-6:]])  # Nur letzte 6
    return f"Aktueller Gesprächsverlauf:\n\n{formatted}"
