import os

BASE_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.2 Agenten/Infrastructure_Agents/MemoryAgent"

MEMORY_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Memory", "memory_log.json")
MEMORY_INDEX_PATH = os.path.join(BASE_PATH, "MemoryAgent_Memory", "memory_index.json")

MEMORY_QUERIES_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Protokolle", "memory_queries_log.json")
MEMORY_REFUSALS_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Protokolle", "memory_refusals_log.json")

# Weitere mögliche Speicherpfade kannst du hier zentral definieren
