# embedding_store.py – Speichert & durchsucht Vektoren (z. B. in JSON-Dateien)

import os
import json
import numpy as np
from typing import List, Dict, Union
from utils.json_loader import load_json, write_json
from agents.General_Agents.RetrievalAgent.similarity_tools import cosine_similarity

# 📍 Speicherort der Embedding-Datenbank (in Google Drive)
STORE_FILENAME = "embedding_store.json"

# 🔁 Embedding speichern
def save_embedding(entry_id: str, vector: List[float], metadata: Dict = {}) -> str:
    data = load_json(STORE_FILENAME)
    if isinstance(data, dict) is False:
        data = {}

    data[entry_id] = {
        "vector": vector,
        "metadata": metadata
    }

    result = write_json(STORE_FILENAME, data)
    if isinstance(result, dict) and "success" in result:
        return f"✅ Embedding gespeichert für: {entry_id}"
    return f"❌ Fehler beim Speichern: {result.get('error', 'Unbekannt')}"

# 🔍 Ähnlichste Embeddings finden (Top-N nach Cosinus-Ähnlichkeit)
def find_similar_embeddings(query_vector: List[float], top_n: int = 5) -> List[Dict[str, Union[str, float]]]:
    data = load_json(STORE_FILENAME)
    if isinstance(data, dict) is False:
        return [{"error": f"❌ Fehler beim Laden der Embedding-Datenbank."}]

    results = []
    for entry_id, entry in data.items():
        stored_vector = entry.get("vector")
        if not stored_vector:
            continue
        try:
            score = cosine_similarity(query_vector, stored_vector)
            results.append({
                "id": entry_id,
                "score": round(score, 4),
                "metadata": entry.get("metadata", {})
            })
        except Exception:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

# 🧹 Datenbank leeren
def clear_embedding_store() -> str:
    result = write_json(STORE_FILENAME, {})
    if isinstance(result, dict) and "success" in result:
        return "🗑️ Embedding-Datenbank wurde geleert."
    return f"❌ Fehler beim Leeren: {result.get('error', 'Unbekannt')}"
