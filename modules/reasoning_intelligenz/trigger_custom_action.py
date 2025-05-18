# trigger_custom_action.py

from modules.output_infrastruktur.mail_tools import send_reminder_mail
from modules.reasoning_intelligenz.memory_log import add_memory_entry
from modules.output_infrastruktur.document_template_engine import generate_document_from_template
from modules.output_infrastruktur.create_text_snippet import create_text_snippet
from modules.reasoning_intelligenz.append_to_trigger_log import append_trigger_log

def execute_trigger_action(trigger: dict) -> str:
    action = trigger.get("action")
    agent = trigger.get("agent", "System")
    project = trigger.get("project", "2.0_GORDON_HOLDING")

    try:
        if action == "send_status_report":
            text = create_text_snippet(project_key=project, context="statusbericht")
            send_reminder_mail(
                subject="🧠 Wöchentlicher Statusbericht",
                content=text,
                recipient="office@gordonholding.de"
            )
            append_trigger_log(trigger["name"], "📬 Statusbericht gesendet")
            return "📬 Statusbericht gesendet"

        elif action == "log_memory_entry":
            add_memory_entry({
                "agent": agent,
                "type": "trigger_log",
                "content": f"Trigger '{trigger['name']}' wurde automatisch ausgeführt.",
                "project": project
            })
            append_trigger_log(trigger["name"], "📝 Memory-Eintrag erstellt")
            return "📝 Memory-Eintrag erstellt"

        elif action == "generate_contract":
            result = generate_document_from_template(
                doc_id=trigger["doc_id"],
                placeholders=trigger["placeholders"],
                replacements=trigger["replacements"]
            )
            append_trigger_log(trigger["name"], f"📄 Vertrag erstellt: {result.get('url')}")
            return f"📄 Vertrag erstellt: {result.get('url')}"

        else:
            append_trigger_log(trigger["name"], f"❌ Aktion '{action}' nicht definiert")
            return f"❌ Aktion '{action}' nicht definiert"

    except Exception as e:
        append_trigger_log(trigger["name"], f"❌ Fehler: {e}")
        return f"❌ Fehler bei Triggeraktion: {e}"
