import os

TELEGRAM_BOT_TOKEN = "5833793075:AAElkx4ei48BA030Jzl_PhKUF6Y72zJkxWQ"
TELEGRAM_CHAT_ID = "-828478140"
TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_ALLOWED_USERS = [5972175655]

GCAL_SCOPES = ["https://www.googleapis.com/auth/calendar"]
GCAL_CAL_ID_PREFIX = "18c770069a5f2babc767018f12cb0ce1f6df9bc3c785a5ce7b468966ceb7ca4c"
GCAL_CAL_ID = f"{GCAL_CAL_ID_PREFIX}@group.calendar.google.com"
GCAL_CLIENT_SECRET = "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"
GCAL_OAUTH_CREDS = {
    "installed": {
        "client_id": "505808692622-asdoj2r0mkdp50plbaajclrie2ct55mq.apps.googleusercontent.com",
        "project_id": "bdaylert",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": GCAL_CLIENT_SECRET,
        "redirect_uris": ["http://localhost"],
    }
}
