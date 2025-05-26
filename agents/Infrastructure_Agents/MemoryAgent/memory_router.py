# memory_router.py – GPT-Memory Routing & Steuerlogik

from agents.Infrastructure_Agents.MemoryAgent.memory_log import log_interaction
from agents.Infrastructure_Agents.MemoryAgent.memory_log_search import memory_log_search
from agents.Infrastructure_Agents.MemoryAgent.memory_config import (
    MEMORY_LOG_PATH,
    ENABLE_INDEX_MATCHING,
    ENABLE_ROLE_ROUTING,
    DEFAULT_AGENT_ROLE,
    DEFAULT_MEMORY_CATEGORY,
    PRIORITY_TAGS,
    SENSITIVE_TAGS,
    AUTOSAVE_CATEGORIES
)


def route_memory_entry(entry):
    """
    Routet eine neue GPT-Memory-Antwort basierend auf Konfigurationswerten.
    Zuweisung erfolgt nach Kategorie, Tags, Rollenlogik etc.
    """
    routed_entry = entry.copy()

    # Standardkategorie setzen, falls nicht vorhanden
    if "category" not in routed_entry:
        routed_entry["category"] = DEFAULT_MEMORY_CATEGORY

    # Rolle zuweisen, wenn Routing aktiviert
    if ENABLE_ROLE_ROUTING and "role" not in routed_entry:
        routed_entry["role"] = DEFAULT_AGENT_ROLE

    # Indexlogik (z. B. zur Navigierbarkeit, Tag-Matching)
    if ENABLE_INDEX_MATCHING:
        tags = routed_entry.get("tags", [])
        if any(tag in PRIORITY_TAGS for tag in tags):
            routed_entry["priority"] = "high"
        if any(tag in SENSITIVE_TAGS for tag in tags):
            routed_entry["sensitive"] = True

    return routed_entry


def save_memory_entry(entry, user="System", source="Router"):
    """
    Speichert die finale Memory-Interaktion ins Log.
    Nutzt das zentrale Logging-Modul.
    """
    log_interaction(
        user=user,
        prompt=entry.get("prompt", ""),
        response=entry.get("response", ""),
        path=MEMORY_LOG_PATH
    )
    return {"status": "saved", "path": MEMORY_LOG_PATH}


def retrieve_similar_entries(criteria):
    """
    Führt eine Suchabfrage im Memory-Log durch.
    Liefert strukturierte, gefilterte Ergebnisse.
    """
    result = memory_log_search(criteria)
    return result
