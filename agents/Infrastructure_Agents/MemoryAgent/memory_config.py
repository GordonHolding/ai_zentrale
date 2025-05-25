# memory_config.py – Zentrale Pfaddefinitionen für Memory-Agent

import os

# 🔁 BASISPFAD: GDrive-Verzeichnis der MemoryAgent-Komponenten
BASE_PATH = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.2 Agenten/Infrastructure_Agents/MemoryAgent"

# 🧠 MEMORY: Zentrale Speicherorte für Memory-Daten
MEMORY_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Memory", "memory_log.json")
MEMORY_INDEX_PATH = os.path.join(BASE_PATH, "MemoryAgent_Memory", "memory_index.json")

# 📜 PROTOKOLLE: Weitere Logs für GPT-Abfragen und Verweigerungen
MEMORY_QUERIES_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Protokolle", "memory_queries_log.json")
MEMORY_REFUSALS_LOG_PATH = os.path.join(BASE_PATH, "MemoryAgent_Protokolle", "memory_refusals_log.json")

# 📂 KONTEXTE (optional erweiterbar)
MEMORY_AGENT_PROMPT_PATH = os.path.join(BASE_PATH, "MemoryAgent_Kontexte_Promptweitergaben", "memory_agent_prompt.json")

# ➕ Erweiterbare weitere Speicherpfade (z. B. für:
# MEMORY_SUMMARIES_PATH = os.path.join(BASE_PATH, "MemoryAgent_Memory", "summaries.json")
# MEMORY_FLAGS_PATH = os.path.join(BASE_PATH, "MemoryAgent_Protokolle", "memory_flags.json")
