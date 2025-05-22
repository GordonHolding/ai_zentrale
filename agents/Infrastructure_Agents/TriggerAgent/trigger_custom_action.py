from modules.output_infrastruktur.mail_tools import send_mail
from modules.reasoning_intelligenz.memory_log import add_memory_entry
from modules.output_infrastruktur.document_template_engine import generate_document_from_template
from modules.output_infrastruktur.create_text_snippet import create_text_snippet
from modules.reasoning_intelligenz.append_to_trigger_log import append_trigger_log

def execute_trigger_action(trigger: dict) -> str:
    action = trigger.get("action")
    agent = trigger.get("agent", "System")
    project = trigger.get("project", "2.0_GORDON_HOLDING")
    mail_mode = trigger.get("mail_mode", "save_draft_confirm")  # Dynamischer Mail-Modus

    try:
        if action == "send_status_report":
            text = create_text_snippet(project_key=project, context="statusbericht")
            send_mail(
                recipient="office@gordonholding.de",
                subject="🧠 Wöchentlicher Statusbericht",
                message_text=text,
                html_text=f"<p>{text}</p>",
                attachments=None,
                mail_mode=mail_mode
            )
            append_trigger_log(trigger["name"], f"📤 Statusbericht ausgelöst ({mail_mode})")
            return f"📤 Statusbericht ausgelöst ({mail_mode})"

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

        elif action == "prepare_contract_cancellation":
            text = create_text_snippet(project_key=project, context="kündigung")
            send_mail(
                recipient="partner@firma.com",
                subject="Vertragskündigung",
                message_text=text,
                html_text=f"<p>{text}</p>",
                attachments=None,
                mail_mode=mail_mode
            )
            append_trigger_log(trigger["name"], f"📝 Kündigungsentwurf erstellt ({mail_mode})")
            return f"📝 Kündigungsentwurf erstellt ({mail_mode})"

        elif action == "create_investor_update":
            text = create_text_snippet(project_key=project, context="investorbericht")
            send_mail(
                recipient="investor@netzwerk.de",
                subject="Investor Update",
                message_text=text,
                html_text=f"<p>{text}</p>",
                attachments=None,
                mail_mode=mail_mode
            )
            append_trigger_log(trigger["name"], f"📝 Investor-Update erstellt ({mail_mode})")
            return f"📝 Investor-Update erstellt ({mail_mode})"

        else:
            append_trigger_log(trigger["name"], f"❌ Unbekannte Aktion: '{action}'")
            return f"❌ Unbekannte Aktion: '{action}'"

    except Exception as e:
        append_trigger_log(trigger["name"], f"❌ Fehler bei Ausführung: {e}")
        return f"❌ Fehler bei Triggeraktion: {e}"
