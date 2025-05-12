def format_text_ci_style(text: str) -> str:
    """
    Optimiert Text nach CI-Vorgaben:
    - Absätze harmonisieren
    - Headlines erkennen & formatieren
    - Einrückungen bereinigen
    - Zeilen umbrechen
    """
    lines = text.strip().split("\n")
    formatted = []
    for line in lines:
        if line.strip().endswith(":"):
            formatted.append(f"\n\n{line.strip().upper()}")  # Headlines betonen
        else:
            formatted.append(line.strip())
    return "\n".join(formatted)
