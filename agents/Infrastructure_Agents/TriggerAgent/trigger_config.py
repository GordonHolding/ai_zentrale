# trigger_config.py

TRIGGER_LABELS = {
    "systemguardian_check": "Systemscan / Loganalyse",
    "mail_reply_check": "Unerledigte Mails nach 72h"
}

DEFAULT_INTERVALS = {
    "systemguardian_check": 24,
    "mail_reply_check": 72
}

TRIGGER_STATE_PATH = "agents/Infrastructure_Agents/TriggerAgent/TriggerAgent_Memory/trigger_state.json"
