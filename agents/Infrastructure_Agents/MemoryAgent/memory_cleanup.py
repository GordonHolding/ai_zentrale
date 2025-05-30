# memory_cleanup.py – Wöchentliche & manuelle Bereinigung von Memory-Dateien

import os
import json
import datetime
from agents.Infrastructure_Agents.MemoryAgent import memory_log, memory_config
from utils.json_loader import load_json, write_json

# 🔄 Nur letzte 5 Sessions pro Nutzer in recent_context.json behalten
def cleanup_recent_context():
    file = "recent_context.json"
    data = load_json(file)
    cleaned = {}

    if not isinstance(data, dict):
        return f"❌ Fehler beim Laden von {file}"

    for user_id, sessions in data.items():
        if isinstance(sessions, list):
            cleaned[user_id] = sessions[-5:]  # Letzte 5 Sessions
    return write_json(file, cleaned)

# 🧹 Entferne Einträge aus chat_history_log.json ohne Tag, Summary oder älter als 6 Monate
def cleanup_chat_history():
    file = "chat_history_log.json"
    data = load_json(file)
    if not isinstance(data, list):
        return f"❌ Fehler beim Laden von {file}"

    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
    cleaned = []

    for entry in data:
        ts = entry.get("timestamp")
        if not ts:
            continue
        try:
            entry_time = datetime.datetime.fromisoformat(ts)
        except:
            continue
        if entry_time < six_months_ago:
            continue
        if not entry.get("tags") and not entry.get("summary"):
            continue
        cleaned.append(entry)

    return write_json(file, cleaned)

# 🧽 Entfernt doppelte, leere oder irrelevante Einträge aus memory_log.json
def cleanup_memory_log():
    file = "memory_log.json"
    data = load_json(file)
    seen = set()
    cleaned = []

    for entry in data:
        if not isinstance(entry, dict):
            continue
        key = (entry.get("prompt"), entry.get("response"))
        if not entry.get("prompt") or not entry.get("response"):
            continue
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(entry)

    return write_json(file, cleaned)

# 🧾 Entfernt defekte oder unverbundene Einträge aus memory_index.json
def cleanup_memory_index():
    file = "memory_index.json"
    data = load_json(file)
    if not isinstance(data, dict):
        return f"❌ Fehler beim Laden von {file}"

    valid = {}
    for key, meta in data.items():
        if meta.get("tags") and meta.get("category"):
            valid[key] = meta
    return write_json(file, valid)

# 📊 Generiere Cleanup-Report zur manuellen Bestätigung
def generate_cleanup_report():
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_context": "Wird auf letzte 5 Sessions pro Nutzer reduziert",
        "chat_history_log": "Löscht Einträge ohne Tags/Summary & älter als 6 Monate",
        "memory_log": "Entfernt Duplikate & leere Einträge",
        "memory_index": "Bereinigt defekte Indexeinträge"
    }
    # Speicherort
    path = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemberichte/Memory/"
    filename = f"{datetime.datetime.now().date()}_memory_cleanup_report.json"
    with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return f"📁 Report erstellt: {filename}"

# 🧠 Cleanup-Aufruf (z. B. durch Trigger)
def run_memory_cleanup():
    r1 = cleanup_recent_context()
    r2 = cleanup_chat_history()
    r3 = cleanup_memory_log()
    r4 = cleanup_memory_index()
    r5 = generate_cleanup_report()
    return [r1, r2, r3, r4, r5]
