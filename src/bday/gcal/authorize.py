import pickle
import os.path

from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from bday import settings

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = f"{CURR_DIR}/token"
CREDS_CONFIG_FILE = f"{CURR_DIR}/calcreds.json"


def get_credentials():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            return pickle.load(token)


def authorize():
    creds: Optional[Credentials] = get_credentials()

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or creds.expired:
        flow = InstalledAppFlow.from_client_config(settings.GCAL_OAUTH_CREDS, settings.GCAL_SCOPES)
        creds = flow.run_local_server()

    with open(TOKEN_FILE, "wb") as t:
        pickle.dump(creds, t)

    return creds


if __name__ == "__main__":
    authorize()
