# memory_config.py – Kompatibel mit alten Imports

from agents.Infrastructure_Agents.JsonAgent.json_config import get_json_metadata

MEMORY_LOG_PATH = get_json_metadata("memory_log")["filename"]
MEMORY_INDEX_PATH = get_json_metadata("memory_index")["filename"]
MEMORY_PROMPT_PATH = get_json_metadata("memory_agent_prompt")["filename"]
MEMORY_QUERIES_LOG_PATH = get_json_metadata("memory_queries_log")["filename"]
MEMORY_REFUSALS_LOG_PATH = get_json_metadata("memory_refusals_log")["filename"]

# Speicherstrategie
MAX_MEMORY_ITEMS = 5000
DEFAULT_TTL_DAYS = 365

# Logging
ENABLE_QUERY_LOGGING = True
ENABLE_REFUSAL_LOGGING = True
LOG_ALL_MEMORY_ENTRIES = True

# Routing & Tags
ENABLE_INDEX_MATCHING = True
ENABLE_ROLE_ROUTING = True
DEFAULT_AGENT_ROLE = "MemoryAgent"
DEFAULT_MEMORY_CATEGORY = "System"

PRIORITY_TAGS = ["core", "investor", "high_priority"]
SENSITIVE_TAGS = ["sensible", "private", "legal"]
AUTOSAVE_CATEGORIES = ["Projekt", "System", "Finanzen"]

VERBOSE_MODE = False
