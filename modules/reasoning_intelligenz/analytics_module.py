def basic_stats(numbers: list) -> dict:
    """
    Gibt Durchschnitt, Minimum, Maximum und Median einer Liste von Zahlen zurück.
    """
    import statistics
    if not numbers:
        return {"error": "Keine Daten vorhanden"}
    return {
        "Anzahl": len(numbers),
        "Mittelwert": statistics.mean(numbers),
        "Median": statistics.median(numbers),
        "Minimum": min(numbers),
        "Maximum": max(numbers)
    }
