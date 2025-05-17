# trigger_router.py

from trigger_triggers import (
    trigger_systemguardian_check,
    trigger_mail_reply_check
)

def determine_trigger(user_input):
    user_input = user_input.lower()

    if "systemscan" in user_input or "guardian" in user_input:
        return trigger_systemguardian_check
    elif "mail" in user_input or "72h" in user_input:
        return trigger_mail_reply_check
    else:
        return None

def handle_trigger_input(user_input):
    func = determine_trigger(user_input)
    if func:
        return func()
    else:
        return "❌ Kein gültiger Trigger erkannt."
