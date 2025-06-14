# render_disk_cleaner.py – automatisches Aufräum-Skript bei jedem Deploy
# 🔒 Löscht nur temporäre, lokale Dateien – keine GDrive- oder Systemdateien
# 🧹 Reinigt: ./tmp/, ./output/, ./logs/, __pycache__/, ~/.cache/
# 🎯 Entfernt: .log, .pkl, .png, .pdf, .mp3, .csv – außer sie stammen aus Drive

import os
import shutil
from pathlib import Path

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
                    if VERBOSE:
                        print(f"🧹 Datei gelöscht: {file_path}")
        except Exception as e:
            print(f"⚠️ Fehler beim Löschen von {file_path}: {e}")

def clean_directories():
    """Löscht gesamte temporäre Ordner und Inhalte."""
    for folder in FOLDERS_TO_CLEAN:
        path = Path(folder)
        if path.exists():
            try:
                shutil.rmtree(path)
                if VERBOSE:
                    print(f"🧹 Ordner gelöscht: {path}")
            except Exception as e:
                print(f"⚠️ Fehler beim Löschen von Ordner {path}: {e}")

def run_disk_cleanup():
    print("🧼 Starte Render Disk Cleanup...")
    clean_directories()
    for folder in FOLDERS_TO_CLEAN:
        Path(folder).mkdir(parents=True, exist_ok=True)  # Neu anlegen, wenn gewünscht
    print("✅ Disk Cleanup abgeschlossen.")

# Wird direkt bei Deployment ausgeführt
if __name__ == "__main__":
    run_disk_cleanup()
