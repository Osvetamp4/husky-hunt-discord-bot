from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

class auth:
    def __init__(self, scopes, secret_file, app_name):
        self.scopes = [scopes] if isinstance(scopes, str) else scopes
        self.secret_file = secret_file
        self.token_file = "token.json"

    def getCredentials(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        # If no credentials or expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.secret_file, self.scopes)
                creds = flow.run_local_server(port=0)

            # Save token
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return creds
