def generate_template(template_type):
    templates = {
        "NDA": "Dies ist eine Vertraulichkeitsvereinbarung zwischen...",
        "Kündigung": "Hiermit kündige ich fristgerecht zum...",
    }
    return templates.get(template_type, "Vorlage nicht gefunden.")
