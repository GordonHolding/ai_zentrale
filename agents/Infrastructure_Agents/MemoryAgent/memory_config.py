# memory_config.py

# Zentrale Konfigurationspfade für MemoryAgent

MEMORY_LOG_PATH = "Infrastructure_Agents/MemoryAgent/MemoryAgent_Memory/memory_log.json"
MEMORY_INDEX_PATH = "Infrastructure_Agents/MemoryAgent/MemoryAgent_Memory/memory_index.json"

# Optional: Pfade für spätere Erweiterungen
MEMORY_QUERIES_LOG_PATH = "Infrastructure_Agents/MemoryAgent/MemoryAgent_Protokolle/memory_queries_log.json"
MEMORY_REFUSALS_LOG_PATH = "Infrastructure_Agents/MemoryAgent/MemoryAgent_Protokolle/memory_refusals_log.json"

# Allgemeine Limits / Einstellungen
MAX_MEMORY_ENTRIES = 1000  # Nur die letzten 1000 Einträge aktiv behalten (optional)
MEMORY_SEARCH_DEPTH = 50   # Wie viele Einträge werden bei Suche gescannt
