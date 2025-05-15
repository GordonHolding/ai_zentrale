# memory_triggers.py

def trigger_on_entry(entry):
    """
    Beispiel: Trigger wird ausgelöst, wenn ein neuer Memory-Eintrag hinzugefügt wurde.
    Später nutzbar für Auto-Replies, Erinnerungen, Weiterleitungen.
    """
    entry_type = entry.get("type", "")
    summary = entry.get("summary", "")[:60]
    print(f"[MemoryTrigger] Neuer Eintrag ({entry_type}): {summary}")

    # Beispiel: Trigger bei Bewerbungseintrag
    if entry_type == "mail" and "bewerbung" in summary.lower():
        print("🔁 Trigger: Bewerbung erkannt – Weiterleitung vorbereiten (optional)")
        # Hier könnten Aktionen wie notify_agent() eingebaut werden

    # Beispiel: Trigger bei Einträgen ohne Antwort
    # → später als Reminder-System erweiterbar
