# retrieval_agent.py – steuert Vektor-Retrieval für GPT-Kontext

from agents.General_Agents.RetrievalAgent.embedding_engine import generate_embedding
from agents.General_Agents.RetrievalAgent.embedding_store import (
    search_similar_entries,
    store_embedding_entry
)
from utils.json_loader import load_json
import numpy as np


def retrieve_context(query_text: str, top_k: int = 3) -> str:
    """
    Ruft den GPT-Kontext zum übergebenen Text ab (per Embedding-Suche).
    """
    try:
        query_embedding = generate_embedding(query_text)
        if isinstance(query_embedding, str):
            return f"❌ Fehler beim Generieren des Embeddings: {query_embedding}"

        results = search_similar_entries(query_embedding, top_k=top_k)
        if not results:
            return "⚠️ Keine passenden Kontexte gefunden."

        context_texts = [r['text'] for r in results]
        return "\n---\n".join(context_texts)

    except Exception as e:
        return f"❌ Retrieval-Fehler: {e}"


def add_context_entry(text: str, metadata: dict = None) -> str:
    """
    Fügt einen neuen Wissenseintrag mit Embedding in den Store ein.
    """
    try:
        embedding = generate_embedding(text)
        if isinstance(embedding, str):
            return f"❌ Fehler beim Embedding: {embedding}"

        entry = {
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        result = store_embedding_entry(entry)
        return result

    except Exception as e:
        return f"❌ Einfüge-Fehler: {e}"
