# router_triggers.py

def post_action_trigger(agent, result):
    """
    Optional: Reaktionen nach Agentenausführung.
    """
    print(f"[Trigger] {agent} hat seine Aufgabe abgeschlossen.")
    if agent == "memory":
        print("📥 Erinnerung möglich – Kontext wurde verarbeitet.")
