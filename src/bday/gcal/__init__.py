import re
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build

from bday import settings
from bday.gcal.authorize import authorize


class AddEventArgs:
    def __init__(self, args: str):
        day, month, age, name = re.match(r"(\d{1,2})/(\d{1,2})\s(\d{1,2})\s(.*)", args).groups()
        self.date = datetime.now().replace(month=int(month), day=int(day))
        self.age = int(age)
        self.name = name
        self.now = datetime.now()

    def __iter__(self):
        """This allows to unpack the class (with * notation)"""
        date = self.next_date.strftime("%Y-%m-%d")
        birth = self.birth_date.strftime("%Y-%m-%d")
        return iter((self.name, date, birth))

    @property
    def next_date(self):
        if self.date > self.now:
            return self.date
        return self.date.replace(year=self.date.year + 1)

    @property
    def birth_date(self):
        return self.next_date.replace(year=self.date.year - self.age)

    def telegram_success_msg(self):
        return (
            f"Success! I have added {self.name}. "
            f"Turning {self.age} on {self.next_date.strftime('%d %B %Y')}"
        )


class CalendarEvent:
    bdate_format = "%Y-%m-%d"

    def __init__(self, id, summary: str, start: dict, description: str, **_kwargs):
        self.id = id
        self.summary = summary
        self.description = json.loads(description)
        self.date = datetime.strptime(start.get("date"), self.bdate_format)
        self.state_key = f"{self.date}{self.summary}"
        self.now = datetime.now()
        self.is_today = self.is_equal(self.now)
        self.is_tomorrow = self.is_equal((self.now + timedelta(days=1)))
        self.is_next_week = self.is_equal((self.now + timedelta(days=7)))
        self.should_notify = self.is_today or self.is_tomorrow or self.is_next_week

    def __repr__(self):
        return f"CalendarEvent({self.summary})"

    @property
    def notify_text(self):
        suffix = "next week"
        if self.is_today:
            suffix = "today!"
        elif self.is_tomorrow:
            suffix = "tomorrow."
        return f"It's {self.summary}'s bday {suffix} Turns {self.age}"

    @property
    def age(self):
        now = datetime.now()
        return now.year - datetime.strptime(self.description["birth_date"], self.bdate_format).year

    @property
    def for_telegram(self):
        return f"{self.date.strftime('%d %B')} - {self.summary} (turns {self.age})"

    def is_equal(self, other: datetime):
        return self.date.strftime(self.bdate_format) == other.strftime(self.bdate_format)


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

    def add_event(self, name: str, next_date: datetime, birth_date: datetime):

        return (
            self.events()
            .insert(
                calendarId=self.calendar_id,
                body=dict(
                    summary=name,
                    description=json.dumps(dict(birth_date=birth_date)),
                    start=dict(date=next_date),
                    end=dict(date=next_date),
                    recurrence=["RRULE:FREQ=YEARLY"],
                    reminders=dict(useDefault=True),
                ),
            )
            .execute()
        )
