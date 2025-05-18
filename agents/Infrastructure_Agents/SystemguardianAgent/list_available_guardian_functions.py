# list_available_guardian_functions.py

from agents.Infrastructure_Agents.SystemGuardian.guardian_function_registry import get_guardian_function_registry

def list_available_guardian_functions():
    try:
        registry = get_guardian_function_registry()
        print("📘 Verfügbare SystemGuardian-Funktionen:")
        for key, info in registry.items():
            status = "✅ aktiv" if info.get("enabled") else "⛔ deaktiviert"
            print(f"• {info['description']}  ({key}) – {status}")
    except Exception as e:
        print(f"❌ Fehler beim Laden der Guardian-Registry: {e}")
