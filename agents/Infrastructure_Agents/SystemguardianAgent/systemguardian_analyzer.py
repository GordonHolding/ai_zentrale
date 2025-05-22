import os
import json
from datetime import datetime
from modules.output_infrastruktur.mail_tools import send_mail
from modules.reasoning_intelligenz.append_to_trigger_log import append_trigger_log

GUARDIAN_LOGS = {
    "policy": "0.2 Agenten/Infrastructure_Agents/SystemGuardian/SystemGuardian_Memory/guardian_policy_log.json",
    "security": "0.2 Agenten/Infrastructure_Agents/SystemGuardian/SystemGuardian_Protokolle/security_audit_log.json",
    "triggers": "0.2 Agenten/Infrastructure_Agents/SystemGuardian/SystemGuardian_Protokolle/guardian_trigger_log.json"
}

def analyze_logs_and_notify():
    summary = []

    for label, path in GUARDIAN_LOGS.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
                last_entry = entries[-1] if entries else {}
                summary.append(f"🧾 **{label.upper()}**: {last_entry.get('message', '–')} ({last_entry.get('timestamp', '-')})")
        else:
            summary.append(f"⚠️ **{label.upper()}**: Datei nicht gefunden.")

    mail_body = "\n\n".join(summary)
    subject = f"Systemstatus am {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    result = send_mail(
        recipient="barry@gordonholding.de",
        subject=subject,
        message_text=mail_body,
        html_text=f"<pre>{mail_body}</pre>",
        mail_mode="save_draft_confirm"
    )

    append_trigger_log("Systemanalyse", f"📤 Bericht an Barry vorbereitet.\n{result}")
    return result
