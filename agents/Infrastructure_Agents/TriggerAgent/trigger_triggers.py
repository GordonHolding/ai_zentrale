# trigger_triggers.py – zentrale Triggerfunktionen des Systems

from agents.Infrastructure_Agents.SystemGuardian import systemguardian_analyzer
from modules.ai_intelligenz.time_based_trigger_checker import check_mail_reply_timeout
from modules.output_infrastruktur.drive_indexer import drive_index_summary
from modules.reasoning_intelligenz.reminder_engine import run_reminder_routine

def trigger_systemguardian_check():
    return systemguardian_analyzer.systemguardian_routine()

def trigger_mail_reply_check():
    return check_mail_reply_timeout()

def trigger_scan_drive():
    return drive_index_summary()

def trigger_reminder_check():
    return run_reminder_routine()

