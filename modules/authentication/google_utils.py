from google.oauth2 import service_account
import os

def get_service_account_credentials(account_name="office_gordonholding", scopes=[]):
    base_path = "/etc/secrets"
    key_path = os.path.join(base_path, f"service_account_{account_name}.json")

    return service_account.Credentials.from_service_account_file(
        key_path,
        scopes=scopes
    )
