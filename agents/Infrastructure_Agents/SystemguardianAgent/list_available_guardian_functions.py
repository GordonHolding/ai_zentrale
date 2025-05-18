# list_available_guardian_functions.py

import os

GUARDIAN_DIR = os.path.join("agents", "Infrastructure_Agents", "SystemGuardian")

def list_available_guardian_functions():
    print("🛡️ Verfügbare Guardian-Module & Trigger:")
    for root, dirs, files in os.walk(GUARDIAN_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), GUARDIAN_DIR)
                print(f"• {rel_path}")
