import os

GUARDIAN_BASE_PATH = "0.2 Agenten/Infrastructure_Agents/SystemGuardian"

LOG_PATHS = {
    "policy": os.path.join(GUARDIAN_BASE_PATH, "SystemGuardian_Memory", "guardian_policy_log.json"),
    "security": os.path.join(GUARDIAN_BASE_PATH, "SystemGuardian_Protokolle", "security_audit_log.json"),
    "triggers": os.path.join(GUARDIAN_BASE_PATH, "SystemGuardian_Protokolle", "guardian_trigger_log.json")
}

ACCESS_CONTROL_PATH = os.path.join(GUARDIAN_BASE_PATH, "SystemGuardian_Memory", "access_control.json")

GUARDIAN_PROMPT_PATH = os.path.join(
    GUARDIAN_BASE_PATH, "SystemGuardian_Kontexte_Promptweitergaben", "system_guardian_prompt.json"
)

def load_guardian_prompt():
    with open(GUARDIAN_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()
