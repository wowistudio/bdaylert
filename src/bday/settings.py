import os
from dotenv import load_dotenv
from pathlib import Path

# when local development you can store your secret envs in <project-root>/local/.env
if os.path.exists(os.environ.get("DOTENV_FILE", "")):
    load_dotenv(Path(os.environ.get("DOTENV_FILE")))

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_ALLOWED_USERS = os.environ["TELEGRAM_ALLOWED_USERS"].split(",")

GCAL_SCOPES = ["https://www.googleapis.com/auth/calendar"]
GCAL_CAL_ID_PREFIX = "18c770069a5f2babc767018f12cb0ce1f6df9bc3c785a5ce7b468966ceb7ca4c"
GCAL_CAL_ID = f"{GCAL_CAL_ID_PREFIX}@group.calendar.google.com"
GCAL_OAUTH_CREDS = {
    "installed": {
        "client_id": os.environ["GCAL_CLIENT_ID"],
        "project_id": "bdaylert",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.environ["GCAL_CLIENT_SECRET"],
        "redirect_uris": ["http://localhost"],
    }
}
