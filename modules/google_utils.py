from google.oauth2 import service_account

def get_credentials(scopes):
    return service_account.Credentials.from_service_account_file(
        "/etc/secrets/service_account_office_at_gordonholding.json",
        scopes=scopes
    )
