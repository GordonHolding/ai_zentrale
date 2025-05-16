import shutil
import datetime
import os

# Speicherort – absoluter Pfad ins Google Drive Verzeichnis
UPLOAD_DIR = "/Users/data/Library/CloudStorage/GoogleDrive-office@gordonholding.de/My Drive/AI-Zentrale/0.0 SYSTEM & KI-GRUNDBASIS/0.3 AI-Regelwerk & Historie/Systemregeln/Chat-History/Uploads"

def save_uploaded_file(user_id: str, file_path: str, original_filename: str, description: str):
    """
    Speichert eine Datei im Upload-Verzeichnis, benennt sie chronologisch und verlinkt sie im Chatverlauf.
    """
    # Zeitstempel + Dateiname
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{timestamp}__{original_filename}"
    full_target_path = os.path.join(UPLOAD_DIR, filename)

    # Datei kopieren
    shutil.copy(file_path, full_target_path)

    # GPT-Verknüpfung: Chatverlauf um Hinweis erweitern
    try:
        from modules.reasoning_intelligenz.conversation_tracker import attach_file_summary
        attach_file_summary(user_id, f"{description} → gespeichert unter {filename}")
    except Exception as e:
        print(f"❌ Fehler beim Verknüpfen des Uploads im Memory: {e}")
