# trigger_triggers.py

from agents.Infrastructure_Agents.SystemGuardian import systemguardian_analyzer
from modules.ai_intelligenz.time_based_trigger_checker import check_mail_reply_timeout

def trigger_systemguardian_check():
    return systemguardian_analyzer.systemguardian_routine()

def trigger_mail_reply_check():
    return check_mail_reply_timeout()
