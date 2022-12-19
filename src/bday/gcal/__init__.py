import pickle
import os.path

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from bday import settings
from bday.gcal.authorize import authorize


class CalendarEvent:
    def __init__(self, id, summary: str, start: dict, **_kwargs):
        self.id = id
        self.summary = summary
        self.date: str = start.get("dateTime") or start.get("date")

    def __repr__(self):
        return f"CalendarEvent({self.summary})"

    @property
    def state_key(self):
        return f"{self.date}{self.summary}"

    @property
    def is_today(self):
        return self.date.startswith(datetime.now().strftime("%Y-%m-%d"))

    @property
    def is_next_week(self):
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        return self.date.startswith(next_week)

    @property
    def for_telegram(self):
        return f"{self.date} - {self.summary}"


class CalendarClient:
    calendar_id = settings.GCAL_CAL_ID

    @staticmethod
    def get_calendar_service():
        return build("calendar", "v3", credentials=authorize())

    def events(self):
        return self.get_calendar_service().events()

    def upcoming(self, limit=10):
        events_result = (
            self.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=datetime.utcnow().isoformat() + "Z",
                maxResults=limit,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return [CalendarEvent(**event) for event in events_result.get("items", [])]

    def add_event(self, date, name):
        return (
            self.events()
            .insert(
                calendarId=self.calendar_id,
                body=dict(
                    summary=name,
                    start=dict(date=date),
                    end=dict(date=date),
                    recurrence=["RRULE:FREQ=YEARLY"],
                    reminders=dict(useDefault=True),
                ),
            )
            .execute()
        )


if __name__ == "__main__":
    print(CalendarClient().upcoming())
