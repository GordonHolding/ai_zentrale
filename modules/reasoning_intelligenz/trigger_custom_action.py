# trigger_custom_action.py

from modules.output_infrastruktur.mail_tools import send_reminder_mail  # optional
from modules.reasoning_intelligenz.memory_log import add_memory_entry  # optional
from modules.output_infrastruktur.text_creator import create_text_snippet  # optional
from modules.output_infrastruktur.document_template_engine import generate_document_from_template  # optional

def execute_trigger_action(trigger: dict) -> str:
    action = trigger.get("action")
    agent = trigger.get("agent", "System")
    project = trigger.get("project", "2.0_GORDON_HOLDING")

    # Beispielaktionen
    if action == "send_status_report":
        # Statusbericht generieren (als Text)
        text = create_text_snippet(project_key=project, context="status")
        send_reminder_mail(
            subject="🧠 Wöchentlicher Statusbericht",
            content=text,
            recipient="office@gordonholding.de"
        )
        return "📬 Statusbericht gesendet"

    elif action == "log_memory_entry":
        add_memory_entry({
            "agent": agent,
            "type": "trigger_log",
            "content": f"Trigger '{trigger['name']}' wurde automatisch ausgeführt.",
            "project": project
        })
        return "📝 Memory-Eintrag erstellt"

    elif action == "generate_contract":
        result = generate_document_from_template(
            doc_id=trigger["doc_id"],
            placeholders=trigger["placeholders"],
            replacements=trigger["replacements"]
        )
        return f"📄 Vertrag erstellt: {result.get('url')}"

    else:
        return f"❌ Aktion '{action}' nicht definiert"
