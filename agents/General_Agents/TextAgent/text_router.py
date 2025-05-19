# text_router.py – GPT-Einbindung: Anfragen dispatchen an Template-Logik

from agents.General_Agents.TextAgent.text_agent import generate_text_from_template

def handle_text_request(context: dict):
    template_key = context.get("template")
    variables = context.get("variables", {})
    if not template_key or not variables:
        return "❌ Unvollständiger Textauftrag."

    return generate_text_from_template(template_key, variables)
