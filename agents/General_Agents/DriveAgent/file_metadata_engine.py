# agents/General_Agents/DriveAgent/file_metadata_engine.py

from utils.json_loader import load_json, write_json
from datetime import datetime

META_PATH = "0.2 Agenten/General_Agents/DriveAgent/DriveAgent_Memory/file_structure_meta.json"

def enrich_file_metadata(file_list):
    """
    Ergänzt Dateiobjekte um strategische Metadaten für GPT-Verarbeitung, Sensitivität, Kategorisierung usw.
    """
    enriched_files = []

    for f in file_list:
        enriched = dict(f)
        name = f.get("name", "").lower()
        path = f.get("path", "").lower()

        # 1. Typklassifikation
        if f.get("mimeType", "").startswith("application/json") or name.endswith(".json"):
            enriched["type"] = "json"
        elif "text" in f.get("mimeType", "") or name.endswith((".txt", ".md")):
            enriched["type"] = "text"
        elif name.endswith((".png", ".jpg", ".jpeg", ".gif")):
            enriched["type"] = "image"
        elif name.endswith((".mp3", ".wav", ".m4a")):
            enriched["type"] = "audio"
        elif name.endswith((".mp4", ".mov", ".avi")):
            enriched["type"] = "video"
        elif name.endswith((".py", ".js", ".html", ".css")):
            enriched["type"] = "code"
        else:
            enriched["type"] = "unknown"

        # 2. Kategorie
        if "zugangsdaten" in path:
            enriched["category"] = "Zugangsdaten"
        elif "verträge" in path:
            enriched["category"] = "Verträge"
        elif "kunden" in path:
            enriched["category"] = "Kunden"
        else:
            enriched["category"] = "Allgemein"

        # 3. Sensitivität
        enriched["sensitive"] = any(x in name for x in ["passwort", "geheim", "login", "zugang"])
        enriched["comment_required"] = enriched["sensitive"] or enriched["category"] in ["Zugangsdaten", "Verträge"]

        # 4. GPT-Kompatibilität
        enriched["gpt_context_enabled"] = enriched["type"] in ["text", "json", "code"]

        # 5. Zusatzinfos
        enriched["watcher_detected"] = True
        enriched["enriched_at"] = datetime.now().isoformat()

        enriched_files.append(enriched)

    try:
        existing = load_json(META_PATH)
    except:
        existing = []

    updated = existing + enriched_files
    write_json(META_PATH, updated)

    return enriched_files
