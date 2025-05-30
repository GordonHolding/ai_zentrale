# drive_agent.py – Zentrale Steuerung für GDrive-Aktionen

from agents.General_Agents.DriveAgent.drive_utils import (
    move_file_or_folder,
    rename_file_or_folder,
    find_files,
    summarize_folder,
    extract_metadata,
    convert_file_to_pdf,
    check_permissions,
    append_entry_to_drive_json  # <- für Logging
)

class DriveAgent:
    def __init__(self, account_name="office_gordonholding"):
        self.account_name = account_name

    def move(self, file_id, new_parent_id):
        return move_file_or_folder(file_id, new_parent_id, self.account_name)

    def rename(self, file_id, new_name):
        return rename_file_or_folder(file_id, new_name, self.account_name)

    def search(self, query):
        return find_files(query, self.account_name)

    def summarize(self, folder_id):
        return summarize_folder(folder_id, self.account_name)

    def metadata(self, file_id):
        return extract_metadata(file_id, self.account_name)

    def convert(self, file_id, export_mime="application/pdf"):
        return convert_file_to_pdf(file_id, export_mime, self.account_name)

    def permissions(self, file_id):
        return check_permissions(file_id, self.account_name)

    def append_log_entry(self, log_path: str, entry: dict):
        """
        Fügt einen Log-Eintrag in eine JSON-Datei im Drive hinzu.
        Nutzt append_entry_to_drive_json aus drive_utils.
        """
        return append_entry_to_drive_json(log_path, entry, self.account_name)
