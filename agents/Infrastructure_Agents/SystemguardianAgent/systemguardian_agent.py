# systemguardian_agent.py – Zentrale Überwachungseinheit für Richtlinien & Systemverhalten

import os
import json
from datetime import datetime

GUARDIAN_PATH = "0.2 Agenten/Infrastructure_Agents/SystemGuardian"

LOGS = {
    "trigger": os.path.join(GUARDIAN_PATH, "SystemGuardian_Protokolle", "guardian_trigger_log.json"),
    "security": os.path.join(GUARDIAN_PATH, "SystemGuardian_Protokolle", "security_audit_log.json"),
    "policy": os.path.join(GUARDIAN_PATH, "SystemGuardian_Memory", "guardian_policy_log.json")
}

ACCESS_CONTROL = os.path.join(GUARDIAN_PATH, "SystemGuardian_Memory", "access_control.json")


def log_guardian_event(log_type, message):
    path = LOGS.get(log_type)
    if not path:
        return
    entry = {
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    entries = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)
    entries.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def check_access_violation(agent: str, action: str):
    if not os.path.exists(ACCESS_CONTROL):
        return False
    with open(ACCESS_CONTROL, "r") as f:
        rules = json.load(f)
    allowed = rules.get(agent, [])
    if action not in allowed:
        log_guardian_event("policy", f"Verbotene Aktion erkannt: {agent} versuchte '{action}'")
        return True
    return False


def guardian_health_report():
    report = {}
    for key, path in LOGS.items():
        if os.path.exists(path):
            with open(path, "r") as f:
                entries = json.load(f)
                report[key] = entries[-3:]  # letzte 3 Einträge
        else:
            report[key] = ["Keine Datei gefunden"]
    return report


if __name__ == "__main__":
    print("SystemGuardian Check gestartet...")
    print(json.dumps(guardian_health_report(), indent=2, ensure_ascii=False))
