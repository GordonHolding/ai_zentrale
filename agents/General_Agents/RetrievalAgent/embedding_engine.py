# embedding_engine.py – wandelt Text in Vektoren (MiniLM oder OpenAI)

import os
from typing import List, Union
from sentence_transformers import SentenceTransformer
import openai
from utils.json_loader import load_json

# 🔧 Lade Modus aus JSON
config = load_json("retrieval_config.json")
MODE = config.get("mode", "local").lower()

LOCAL_MODEL_PATH = "General_Agents/RetrievalAgent/Model/all-MiniLM-L6-v2"
_model = None

def load_local_model():
    global _model
    if _model is None:
        if not os.path.exists(LOCAL_MODEL_PATH):
            return f"❌ Lokales Modell nicht gefunden unter: {LOCAL_MODEL_PATH}"
        _model = SentenceTransformer(LOCAL_MODEL_PATH)
    return _model

def generate_embedding(text: Union[str, List[str]]) -> Union[List[float], str]:
    """
    Wandelt Text in Embeddings um (GPT- oder lokal, je nach retrieval_config.json)
    """
    if MODE == "openai":
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            return f"❌ OpenAI Fehler: {e}"

    elif MODE == "local":
        try:
            model = load_local_model()
            embedding = model.encode(text, convert_to_numpy=True).tolist()
            return embedding
        except Exception as e:
            return f"❌ Lokaler Embedding-Fehler: {e}"

    else:
        return f"❌ Ungültiger Modus in retrieval_config.json: '{MODE}'"
