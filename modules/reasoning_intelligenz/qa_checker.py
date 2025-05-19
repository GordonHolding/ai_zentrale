# qa_checker.py

def check_text_quality(text: str) -> dict:
    """
    Prüft, ob Text CI-Anforderungen erfüllt:
    – Länge pro Absatz
    – Verwendung typischer Füllwörter
    – Vorhandensein einer Headline
    """
    errors = []

    if len(text) < 200:
        errors.append("Text ist sehr kurz – möglicherweise nicht aussagekräftig.")

    if any(w in text.lower() for w in ["eigentlich", "sozusagen", "eventuell"]):
        errors.append("Text enthält unscharfe Füllwörter.")

    if ":" not in text:
        errors.append("Es scheint keine strukturierte Headline vorhanden zu sein.")

    return {
        "status": "ok" if not errors else "warnung",
        "hinweise": errors
    }
