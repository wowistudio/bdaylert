import dataclasses
import socket

from bday.telegram import Telegram
from bday.gcal import CalendarClient, AddEventArgs
from bday.notify import handle_notify

HELP = """
/ping - Check alive
/upcoming - Show upcoming bdays
/add - Add new bday ([day]/[month] [age] [name]")
/dryrun - Notify, don't save
/help - Show this list
"""


class Commands(type):
    store = {}

    def __new__(mcs, name, bases, dikt):
        klass = type.__new__(mcs, name, bases, dikt)
        if hasattr(klass, "name"):
            klass = dataclasses.dataclass(klass)
            assert klass.name not in mcs.store
            mcs.store[klass.name] = klass
        return klass

    @classmethod
    def get(mcs, command: str, args: str, telegram: Telegram):
        return mcs.store[command](telegram=telegram, args=args)


@dataclasses.dataclass
class Command(metaclass=Commands):
    telegram: Telegram
    args: str


class Ping(Command):
    name = "ping"

    def call(self):
        self.telegram.send(f"👋 Hi from {socket.gethostname()}")


class Help(Command):
    name = "help"

    def call(self):
        self.telegram.send(HELP)


class Upcoming(Command):
    name = "upcoming"
    client = CalendarClient()

    def call(self):
        events = [event.for_telegram for event in self.client.upcoming()]
        self.telegram.send("\n".join(events))


class DryRun(Command):
    name = "dryrun"

    def call(self):
        handle_notify()


class Add(Command):
    name = "add"
    client = CalendarClient()

    def call(self):
        try:
            event_args = AddEventArgs(self.args)
            self.client.add_event(*event_args)
            self.telegram.send(event_args.telegram_success_msg())
        except Exception as e:
            print("ERROR", e)
            self.telegram.send("Wrong payload. Send like: /add [month]/[day] [age] [name]")
