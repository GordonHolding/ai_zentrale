# utils/render_disk_cleaner.py
# 🔒 Löscht nur temporäre, lokale Dateien – keine GDrive- oder Systemdateien
# 🧹 Reinigt: ./tmp/, ./output/, ./logs/, __pycache__/, ~/.cache/
# 🎯 Entfernt: .log, .pkl, .png, .pdf, .mp3, .csv, .txt – außer sie stammen aus Drive

import os
import shutil
from pathlib import Path
from datetime import datetime

# Globale Ergebnisse
cleanup_results = {
    "status": "unknown",
    "deleted_files": [],
    "deleted_folders": [],
    "errors": [],
    "timestamp": None
}

# Ordner, die komplett gelöscht werden können
FOLDERS_TO_CLEAN = [
    "./tmp", "./output", "./logs", "__pycache__", os.path.expanduser("~/.cache")
]

# Dateiendungen, die gelöscht werden dürfen
ALLOWED_EXTENSIONS = [".log", ".pkl", ".png", ".pdf", ".mp3", ".csv", ".txt"]

# Optional: Logging-Ausgabe
VERBOSE = True


def clean_folder(folder_path):
    """Löscht alle passenden Dateien innerhalb eines Ordners (rekursiv)."""
    folder = Path(folder_path)
    if not folder.exists():
        return
    for file_path in folder.rglob("*"):
        try:
            if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                if "gdrive" not in str(file_path).lower():
                    file_path.unlink()
                    cleanup_results["deleted_files"].append(str(file_path))
                    if VERBOSE:
                        print(f"🧹 Datei gelöscht: {file_path}")
        except Exception as e:
            cleanup_results["errors"].append(f"{file_path}: {e}")
            print(f"⚠️ Fehler beim Löschen von {file_path}: {e}")


def clean_directories():
    """Löscht ganze temporäre Ordner."""
    for folder in FOLDERS_TO_CLEAN:
        path = Path(folder)
        if path.exists():
            try:
                shutil.rmtree(path)
                cleanup_results["deleted_folders"].append(str(path))
                if VERBOSE:
                    print(f"🧹 Ordner gelöscht: {path}")
            except Exception as e:
                cleanup_results["errors"].append(f"{path}: {e}")
                print(f"⚠️ Fehler beim Löschen von Ordner {path}: {e}")


def run_disk_cleanup():
    """Führt vollständige Bereinigung durch."""
    print("🧼 Starte Render Disk Cleanup...")
    cleanup_results["timestamp"] = datetime.utcnow().isoformat()
    cleanup_results["deleted_files"] = []
    cleanup_results["deleted_folders"] = []
    cleanup_results["errors"] = []

    clean_directories()
    for folder in FOLDERS_TO_CLEAN:
        Path(folder).mkdir(parents=True, exist_ok=True)  # Struktur wiederherstellen
    for folder in FOLDERS_TO_CLEAN:
        clean_folder(folder)

    cleanup_results["status"] = "done"
    print("✅ Disk Cleanup abgeschlossen.")


def get_last_cleanup_report():
    """Gibt die Ergebnisse der letzten Bereinigung zurück (für Monitoring/Health)."""
    return cleanup_results


# Automatisch bei Import aufrufen
run_disk_cleanup()
