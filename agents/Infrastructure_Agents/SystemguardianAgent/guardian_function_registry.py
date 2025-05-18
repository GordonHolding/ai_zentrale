# guardian_function_registry.py

def get_guardian_function_registry():
    return {
        "analyze_logs_and_notify": {
            "description": "📊 Systemanalyse durchführen & Bericht an Barry generieren",
            "enabled": True
        },
        "escalate_security_incident": {
            "description": "🚨 Sicherheitsvorfall eskalieren und Entwurf generieren",
            "enabled": True
        },
        "handle_guardian_input": {
            "description": "🛡️ Manueller Textbefehl (GPT oder Mensch) zur Guardian-Steuerung",
            "enabled": True
        }
    }
