# memory_config.py

from json_config import get_json_metadata

# Dynamisch aus json_memory_index.json geladen
MEMORY_LOG_FILE = get_json_metadata("memory_log")["filename"]
MEMORY_INDEX_FILE = get_json_metadata("memory_index")["filename"]
MEMORY_PROMPT_FILE = get_json_metadata("memory_agent_prompt")["filename"]
MEMORY_QUERIES_LOG_FILE = get_json_metadata("memory_queries_log")["filename"]
MEMORY_REFUSALS_LOG_FILE = get_json_metadata("memory_refusals_log")["filename"]

# Speicherstrategie
MAX_MEMORY_ITEMS = 5000
DEFAULT_TTL_DAYS = 365  # Automatische Löschung nach 1 Jahr (optional)

# Logging
ENABLE_QUERY_LOGGING = True
ENABLE_REFUSAL_LOGGING = True
LOG_ALL_MEMORY_ENTRIES = True  # Auch interne Einträge speichern

# Trigger & Verhalten
ENABLE_INDEX_MATCHING = True
ENABLE_ROLE_ROUTING = True
DEFAULT_AGENT_ROLE = "MemoryAgent"
DEFAULT_MEMORY_CATEGORY = "System"

# Tags für GPT-Auswertung
PRIORITY_TAGS = ["core", "investor", "high_priority"]
SENSITIVE_TAGS = ["sensible", "private", "legal"]
AUTOSAVE_CATEGORIES = ["Projekt", "System", "Finanzen"]

# Debugging
VERBOSE_MODE = False
