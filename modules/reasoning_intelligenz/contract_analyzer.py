def extract_clauses(text):
    important_keywords = ["Kündigungsfrist", "Laufzeit", "Vertraulichkeit", "Lizenz"]
    results = {kw: kw in text for kw in important_keywords}
    return results
