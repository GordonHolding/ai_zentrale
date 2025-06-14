# utils/render_disk_cleaner.py

import os
import shutil
import time

# 🔧 Konfigurierbare Zielverzeichnisse
CLEAN_PATHS = [
    "/tmp",
    "./tmp",
    "./output",
    "./logs",
    "./__pycache__",
    os.path.expanduser("~/.cache")
]

# 🔍 Ziel-Dateiendungen (temporär, speicherintensiv)
TARGET_EXTENSIONS = [".log", ".pkl", ".png", ".pdf", ".mp3", ".csv"]

# 📝 Cleanup-Report
cleanup_results = {
    "status": "not started",
    "start_time": None,
    "end_time": None,
    "deleted_files": [],
    "errors": []
}


def clean_path(path):
    """
    Löscht gezielt Dateien in einem Verzeichnis – rekursiv & selektiv.
    """
    deleted = []
    if not os.path.exists(path):
        return deleted

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full_path = os.path.join(root, name)
            if any(name.lower().endswith(ext) for ext in TARGET_EXTENSIONS):
                try:
                    os.remove(full_path)
                    deleted.append(full_path)
                except Exception as e:
                    cleanup_results["errors"].append(f"{full_path}: {e}")
        for name in dirs:
            full_dir = os.path.join(root, name)
            if "__pycache__" in full_dir or full_dir.endswith("/__pycache__"):
                try:
                    shutil.rmtree(full_dir)
                    deleted.append(full_dir)
                except Exception as e:
                    cleanup_results["errors"].append(f"{full_dir}: {e}")
    return deleted


def main():
    """
    Hauptfunktion – führt Cleanup durch und speichert Ergebnisse.
    """
    cleanup_results["status"] = "started"
    cleanup_results["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

    all_deleted = []
    for path in CLEAN_PATHS:
        deleted = clean_path(path)
        all_deleted.extend(deleted)

    cleanup_results["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    cleanup_results["deleted_files"] = all_deleted
    cleanup_results["status"] = "done"
    print(f"[🧹 RenderDiskCleaner] Bereinigt {len(all_deleted)} Datei(en).")


def get_last_cleanup_report():
    """
    Liefert den letzten Cleanup-Status für Monitoring oder HealthCheck.
    """
    return cleanup_results


# 🚀 Cleanup automatisch starten (bei Import)
main()
