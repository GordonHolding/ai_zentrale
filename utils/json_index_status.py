# json_index_status.py
# 🧠 Statusmodul zur Überprüfung geladener JSON-Dateien im Vergleich zum zentralen Index (json_file_index.json)
# ✅ Vergleicht RAM-Inhalte aus context_memory mit json_file_index.json
# 🌍 Zeigt: geladene, fehlende, veraltete Dateien (per last_checked)

import datetime
from utils.context_memory import get_all_context
from utils.json_loader import load_json, safe_load_json

# Konfigurierbare Schwelle (in Tagen) zur Verfallsanzeige
MAX_AGE_DAYS = 3


def flatten_index(index: dict) -> dict:
    """Flacht die Indexstruktur zu einem Dictionary mit Dateinamen als Schlüssel ab."""
    flat = {}

    def _recurse(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, dict) and val.get("path") and val.get("drive_id"):
                    name = val["path"].split("/")[-1]
                    flat[name] = val
                else:
                    _recurse(val)
        elif isinstance(obj, list):
            for item in obj:
                _recurse(item)

    _recurse(index)
    return flat


def parse_timestamp(ts: str) -> datetime.datetime:
    try:
        return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return datetime.datetime.min


def check_json_index_status():
    context = get_all_context()
    index_data = load_json("json_file_index.json")
    flat_index = flatten_index(index_data)

    loaded_files = set(context.keys())
    indexed_files = set(flat_index.keys())

    missing = sorted(list(indexed_files - loaded_files))
    loaded = sorted(list(indexed_files & loaded_files))

    outdated = []
    now = datetime.datetime.utcnow()
    for name in loaded:
        meta = flat_index.get(name, {})
        ts = parse_timestamp(meta.get("last_checked", ""))
        if (now - ts).days > MAX_AGE_DAYS:
            outdated.append({
                "filename": name,
                "last_checked": meta.get("last_checked")
            })

    return {
        "total_indexed": len(indexed_files),
        "loaded_in_memory": len(loaded_files),
        "missing_from_memory": missing,
        "outdated_in_memory": outdated
    }


if __name__ == "__main__":
    import json
    print(json.dumps(check_json_index_status(), indent=2, ensure_ascii=False))
