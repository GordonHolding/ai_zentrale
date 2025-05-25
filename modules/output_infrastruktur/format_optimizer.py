# format_optimizer.py – Optimiert Text nach CI-Vorgaben

def format_text_ci_style(text: str) -> str:
    """
    Optimiert Text nach CI-Vorgaben:
    – Absätze harmonisieren
    – Headlines erkennen & formatieren
    – Einrückungen bereinigen
    – Zeilen umbrechen
    """
    lines = text.strip().split("\n")
    formatted = []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        if clean.endswith(":"):
            formatted.append(f"\n\n{clean.upper()}")  # Headlines betonen
        else:
            formatted.append(clean)

    return "\n".join(formatted)
