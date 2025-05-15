# interface_triggers.py

def post_action_trigger(agent, result):
    """
    Optional: Triggert Folgeaktionen nach erfolgreicher Ausführung.
    """
    print(f"[Trigger] Aktion von {agent} abgeschlossen.")
    # Beispiel: Bei memory-Antwort automatische Notiz speichern
    if agent == "memory":
        print("📝 Trigger: Ergebnis kann ins Gedächtnis übernommen werden.")
