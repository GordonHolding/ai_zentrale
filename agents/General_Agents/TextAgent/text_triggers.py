# text_triggers.py – Triggerlogik für TextAgent

import datetime
from agents.General_Agents.TextAgent import text_agent
from modules.reasoning_intelligenz import startup_loader
from modules.output_infrastruktur import drive_indexer
from modules.Infrastructure_Agents.MemoryAgent import memory_log

# 📌 Trigger bei Systemstart
def trigger_on_startup():
    timestamp = datetime.datetime.now().isoformat()
    memory_log.log_system_start(entries=[
        f"[TextAgent] Initialisiert um {timestamp}",
        "Trigger: trigger_on_startup()",
        "Status: Bereit für Textanalysen und Eingaben"
    ])
    print("✅ TextAgent bereit (Startup Trigger)")

# 🧠 Trigger durch Chainlit / GPT / API
def trigger_on_input(input_text: str, metadata: dict = None):
    try:
        response = text_agent.process_text(input_text)
        log_routing(input_text, response)
        return response
    except Exception as e:
        memory_log.log_mail_entry(
            mail_id="TEXT-TRIGGER-ERROR",
            sender="system",
            subject="TextAgent Trigger Error",
            category="trigger",
            summary=str(e)
        )
        return f"[Fehler im TextAgent Trigger]: {str(e)}"

# 🧾 Logging der Trigger-Aktivität
def log_routing(input_text, result):
    routing_log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": "TextAgent",
        "trigger": "trigger_on_input",
        "input_preview": input_text[:100],
        "output_preview": str(result)[:100]
    }
    drive_indexer.append_to_log("driveagent_routing_log.json", routing_log)
