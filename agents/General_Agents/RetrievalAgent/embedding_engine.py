# embedding_engine.py

import os
from typing import List, Union
from sentence_transformers import SentenceTransformer
from utils.json_loader import load_json
import openai

# 🔧 Modus aus Konfigurationsdatei
config = load_json("retrieval_config.json")
MODE = config.get("mode", "local").strip().lower()

# 📁 Lokaler Modellpfad
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_MODEL_PATH = os.path.join(BASE_DIR, "Model", "all-MiniLM-L6-v2")

_model = None

def load_local_model():
    """
    Lädt MiniLM-Modell nur einmal (Lazy Load)
    """
    global _model
    if _model is None:
        if not os.path.exists(LOCAL_MODEL_PATH):
            raise FileNotFoundError(f"❌ Lokales Modell nicht gefunden unter: {LOCAL_MODEL_PATH}")
        try:
            _model = SentenceTransformer(LOCAL_MODEL_PATH)
        except Exception as e:
            raise RuntimeError(f"❌ Fehler beim Laden des lokalen Modells: {e}")
    return _model

def generate_embedding(text: Union[str, List[str]]) -> Union[List[float], str]:
    """
    Wandelt Text in Embedding um – je nach Modus via OpenAI oder lokal.
    Gibt im Fehlerfall GPT-kompatible Fehlermeldung zurück.
    """
    try:
        if MODE == "openai":
            if not openai.api_key:
                return "❌ OpenAI-API-Key fehlt. Bitte setzen in Umgebungsvariablen."
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response["data"][0]["embedding"]

        elif MODE == "local":
            model = load_local_model()
            return model.encode(text, convert_to_numpy=True).tolist()

        else:
            return f"❌ Ungültiger Modus in retrieval_config.json: '{MODE}'"

    except Exception as e:
        source = "OpenAI" if MODE == "openai" else "lokal"
        return f"❌ {source}-Embedding-Fehler: {str(e)}"
