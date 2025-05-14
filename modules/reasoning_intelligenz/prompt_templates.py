# prompt_templates.py

TEMPLATES = {
    "dresscode_answer": {
        "style": "casual, cool, markenbewusst",
        "prefix": "Hey! Danke für deine Nachricht – hier ist, was ich dazu sagen würde:",
        "suffix": "Wenn du noch was brauchst, sag Bescheid!"
    },
    "gordonholding_reply": {
        "style": "seriös, professionell, effizient",
        "prefix": "Sehr geehrte Damen und Herren,",
        "suffix": "Mit freundlichen Grüßen,\nBarry Gordon"
    },
    "ai_zentrale_system": {
        "style": "neutral, analytisch, KI-assistententauglich",
        "prefix": "Systemantwort:",
        "suffix": "Ende der Antwort."
    }
}

def get_prompt_template(profile="gordonholding_reply"):
    return TEMPLATES.get(profile, TEMPLATES["ai_zentrale_system"])
